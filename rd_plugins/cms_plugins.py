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

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext_lazy as _

from .models import RdTranslationAvailable

@plugin_pool.register_plugin
class RdI18nPlugin(CMSPluginBase):

    model = RdTranslationAvailable
    name = _("Available Translations")
    module = 'Chessdevil'
    render_template = "rd_plugins/available_languages.html"

    def render(self, context, instance, placeholder):
        context['lang'] = context['targetlang'] if 'targetlang' in context \
            else context['language']
        context = super(RdI18nPlugin, self).render(
            context, instance, placeholder)
        return context


from .models import (
    RdGridContainer,
    RdGridLayout,
    RdGridCell,
)

from .constants import GRID_DISPLAYS

@plugin_pool.register_plugin
class RdGridContainerPlugin(CMSPluginBase):

    model = RdGridContainer
    name = _('Container')
    module = 'Chessdevil'
    render_template = 'rd_plugins/grid_container.html'
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
    module = 'Chessdevil'
    render_template = 'rd_plugins/grid_layout.html'
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
    module = 'Chessdevil'
    render_template = 'rd_plugins/grid_cell.html'
    allow_children = True
    require_parent = True
    parent_classes = ['RdGridLayoutPlugin']

    def render(self, context, instance, placeholder):
        cells = []
        offsets = []
        for d in GRID_DISPLAYS:
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
