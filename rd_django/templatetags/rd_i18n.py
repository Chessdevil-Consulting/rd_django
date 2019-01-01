#    Copyright 2017 - 2018 Ruben Decrop
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.


# this module is derived from django.templatetags.i18n
# goal it to use the language files stored in static/lang/{language}.json
# as translations source iso using the gettext .mo files
# as such we have a unified translation strategy for vue and django

import logging
log = logging.getLogger(__name__)

import sys
import requests

from django.conf import settings
from django.template import Library, Node, TemplateSyntaxError, Variable
from django.template.base import TOKEN_TEXT, TOKEN_VAR, render_value_in_context
from django.template.defaulttags import token_kwargs
from django.utils import six, translation
from django.utils.safestring import SafeData, mark_safe

register = Library()

translation_strings = {}

def read_translation_files(request):
    """
    read all translation files  in /static/lang
    and store them in translation_strings
    :return:
    """
    if len(translation_strings):
        return
    languages = settings.LANGUAGES
    sturl = settings.STATIC_URL
    for l,lt in languages:
        try:
            url = request.build_absolute_uri("{0}lang/{1}.json".format(sturl, l))
            r = requests.get(url)
            if r.status_code != 200:
                log.warning('cannot read lang file {0}: {1}'.format(
                    url, r.reason))
                continue
            translation_strings[l] = r.json()
        except Exception as e:
            log.error('Error reading json language file for %s', l)
            raise e

class GetCurrentLanguageNode(Node):
    def __init__(self, variable):
        self.variable = variable

    def render(self, context):
        context[self.variable] = translation.get_language()
        return ''

class TranslateNode(Node):

    def __init__(self, filter, asvar=False):
        self.filter = filter
        self.asvar = asvar

    def render(self, context):
        read_translation_files(context.request)
        lang = translation.get_language()
        value = translation_strings[lang].get(self.filter.var)
        if not value:
            log.warning('no %s translation for %s', lang, self.filter)
        if self.asvar:
            context[self.asvar] = value
            return ''
        else:
            return value

class BlockTranslateNode(Node):

    def __init__(self, singular, ):
        self.singular = singular

    def render_token_list(self, tokens):
        result = []
        vars = []
        for token in tokens:
            if token.token_type == TOKEN_TEXT:
                result.append(token.contents.replace('%', '%%'))
            elif token.token_type == TOKEN_VAR:
                result.append('%%(%s)s' % token.contents)
                vars.append(token.contents)
        msg = ''.join(result)
        return msg, vars

    def render(self, context, nested=False):
        read_translation_files(context.request)
        message_context = None
        tmp_context = {}
        singular, vars = self.render_token_list(self.singular)
        result = translation.ugettext(singular)
        default_value = context.template.engine.string_if_invalid

        def render_value(key):
            if key in context:
                val = context[key]
            else:
                val = default_value % key if '%s' in default_value else default_value
            return render_value_in_context(val, context)

        data = {v: render_value(v) for v in vars}
        context.pop()
        try:
            result = result % data
        except (KeyError, ValueError):
            if nested:
                # Either string is malformed, or it's a bug
                raise TemplateSyntaxError(
                    "'blocktrans' is unable to format string returned by gettext: %r using %r"
                    % (result, data)
                )
            with translation.override(None):
                result = self.render(context, nested=True)
        return result

@register.tag("get_current_language")
def do_get_current_language(parser, token):
    """
    This will store the current language in the context.

    Usage::

        {% get_current_language as language %}

    This will fetch the currently active language and
    put it's value into the ``language`` context
    variable.
    """
    # token.split_contents() isn't useful here because this tag doesn't accept variable as arguments
    args = token.contents.split()
    if len(args) != 3 or args[1] != 'as':
        raise TemplateSyntaxError("'get_current_language' requires 'as variable' (got %r)" % args)
    return GetCurrentLanguageNode(args[2])

@register.tag("trans")
def do_translate(parser, token):
    """
    This will mark a string for translation and will
    translate the string for the current language.

        {% trans "this is a test" %}

    You can use variables instead of constant strings
    to translate stuff you marked somewhere else::

        {% trans variable %}

    This will just try to translate the contents of
    the variable ``variable``. Make sure that the string
    in there is something that is in the trnalsation files.

    It is possible to store the translated string into a variable::

        {% trans "this is a test" as var %}
        {{ var }}

    """
    bits = token.split_contents()
    if len(bits) < 2:
        raise TemplateSyntaxError("'%s' takes at least one argument" % bits[0])
    message_string = parser.compile_filter(bits[1])
    remaining = bits[2:]
    asvar = None

    while remaining:
        option = remaining.pop(0)
        if option == 'as':
            try:
                value = remaining.pop(0)
            except IndexError:
                msg = "No argument provided to the '%s' tag for the as option." % bits[0]
                six.reraise(TemplateSyntaxError, TemplateSyntaxError(msg), sys.exc_info()[2])
            asvar = value
        else:
            raise TemplateSyntaxError(
                "Unknown argument for '%s' tag: '%s'. The only option "
                "available is 'as VAR'." % (bits[0], option,)
            )
    return TranslateNode(message_string)


@register.tag("blocktrans")
def do_block_translate(parser, token):
    """
    This will translate a block of text with parameters.

    Usage::

        {% blocktrans %}
        This is {{ bar }}s and {{ boo }}.
        {% endblocktrans %}

    """
    countervar, counter = None, None
    message_context = None
    singular = []
    plural = []
    while parser.tokens:
        token = parser.next_token()
        if token.token_type in (TOKEN_VAR, TOKEN_TEXT):
            singular.append(token)
        else:
            break
    if token.contents.strip() != 'endblocktrans':
        raise TemplateSyntaxError("'blocktrans' doesn't allow other block tags (seen %r) inside it" % token.contents)

    return BlockTranslateNode(singular)
