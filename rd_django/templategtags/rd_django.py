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

import logging
log = logging.getLogger(__name__)

from django import template

from cms.models.pagemodel import Page
from cms.models.placeholdermodel import Placeholder
from cms.models.pluginmodel import CMSPlugin
from cms.utils.i18n import get_current_language

register = template.Library()

@register.inclusion_tag('rd_django/tags/render_language_block.html', 
    takes_context=True)
def render_language_block(context, *args):
    page = context.request.current_page
    placeholdername = args[0] if args else 'content'
    log.info('page_id=%d', page.id)
    for pl in page.get_placeholders():
        if pl.slot == placeholdername:
            placeholder = pl
            break
    else:
        raise Placeholder.DoesNotExist()
    published_languages = set()
    for l in page.languages.split(','):
        title = page.get_title_obj(l)
        if not title.publisher_is_draft:
            published_languages.add(l)
    available_languages = set()
    for plg in CMSPlugin.objects.filter(placeholder_id=placeholder.id):
        if plg.language in published_languages:
            available_languages.add(plg.language)
    c = {
        'available_languages': available_languages,
        'language': get_current_language(),
        'request': context.request,
    }
    return c