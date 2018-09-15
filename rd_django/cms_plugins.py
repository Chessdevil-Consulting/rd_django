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

import requests
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.conf import settings # import the settings file
from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import (
    RdGridContainer,
    RdGridLayout,
    RdGridCell,
    RdGridCellConstants,
    RdIcon,
    RdPersonGroup,
    RdPerson,
)

@plugin_pool.register_plugin
class RdGridContainerPlugin(CMSPluginBase):

    model = RdGridContainer
    name = _('Container')
    module = 'Reddevil'
    render_template = 'rd_django/grid_container.html'
    allow_children = True

    def render(self, context, instance, placeholder):
        context['fluid'] = ''
        if instance.container == 'fluid':
            context['fluid'] = 'fluid'
        context['gutter'] = ''
        if instance.gutter:
            context['gutter'] = 'grid-list-{}'.format(instance.gutter)
        return super(RdGridContainerPlugin, self).render(
            context, instance, placeholder)

@plugin_pool.register_plugin
class RdGridLayoutPlugin(CMSPluginBase):

    model = RdGridLayout
    name = _('Layout')
    module = 'Reddevil'
    render_template = 'rd_django/grid_layout.html'
    allow_children = True
    child_classes = ['RdGridCellPlugin']

    def render(self, context, instance, placeholder):
        context['direction'] = 'row'
        if instance.layout == 'vertical':
            context['direction'] = 'column'
        context['wrap'] = ''
        if instance.wrap:
            context['wrap'] = 'wrap'
        return super(RdGridLayoutPlugin, self).render(
            context, instance, placeholder)

@plugin_pool.register_plugin
class RdGridCellPlugin(CMSPluginBase):

    model = RdGridCell
    name = _('Cell')
    module = 'Reddevil'
    render_template = 'rd_django/grid_cell.html'
    allow_children = True
    require_parent = True
    parent_classes = ['RdGridLayoutPlugin']

    def render(self, context, instance, placeholder):
        cells = []
        offsets = []
        for d in RdGridCellConstants.DISPLAYS:
            fieldsize = getattr(instance, '{}_size'.format(d))
            if fieldsize:
                cells.append('{}{}'.format(d, fieldsize))
            fieldoffset = getattr(instance, '{}_offset'.format(d))
            if fieldoffset:
                offsets.append('offset-{}{}'.format(d, fieldoffset))
        context['cells'] = ' '.join(cells) if cells else ''
        context['offsets'] = ' '.join(offsets) if offsets else ''
        return super(RdGridCellPlugin, self).render(
            context, instance, placeholder)

@plugin_pool.register_plugin
class RdIconPlugin(CMSPluginBase):

    model = RdIcon
    name = _('Icon')
    module = 'Reddevil'
    render_template = 'rd_django/icon.html'
    text_enabled = True

    def render(self, context, instance, placeholder):
        context['icon'] = instance.icon
        context['size'] = instance.size
        context['color'] = instance.color
        context['additional_classes'] = ''
        if instance.additional_classes:
            context['additional_classes'] = 'class="{}"'.format(instance.additional_classes)
        return super(RdIconPlugin, self).render(
            context, instance, placeholder)

@plugin_pool.register_plugin
class RdPersonGroupPlugin(CMSPluginBase):

    model = RdPersonGroup
    name = _('Group of persons')
    module = 'Reddevil'
    render_template = 'rd_django/person_group.html'
    allow_children = True
    child_classes = ['RdPersonPlugin']

    def render(self, context, instance, placeholder):
        return super(RdPersonGroupPlugin, self).render(
            context, instance, placeholder)


class RdPersonForm(forms.ModelForm):

    idbel = forms.ChoiceField(choices=('45608','28908'))


@plugin_pool.register_plugin
class RdPersonPlugin(CMSPluginBase):

    model = RdPerson
    name = _('Person')
    module = 'Reddevil'
    render_template = 'rd_django/person.html'
    require_parent = True
    # form = RdPersonForm

    def render(self, context, instance, placeholder):
        ca = settings.CHESSAPI_URL
        group = instance.parent.rd_django_rdpersongroup.group
        rs = requests.get("{}members/member/{}".format(ca, instance.idbel))
        person = rs.json()
        person['role'] = None
        if person.get('photolength'):
            person['photourl'] = "{}members/photo/{}".format(ca, instance.idbel)
        else:
            person['photurl'] = '/static/img/nobody.png'
        for role in person.get('org', []):
            if role.get('group') == group:
                person['role'] = role.get('role')
        context.update(person)
        return super(RdPersonPlugin, self).render(
            context, instance, placeholder)