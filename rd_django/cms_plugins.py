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

from .models import (
    RdBox,
    RdGridContainer,
    RdGridLayout,
    RdGridCell,
    RdGridCellConstants,
    RdIcon,
    RdPersonGroup,
    RdPerson,
    RdTabGroup,
    RdTab,
)

@plugin_pool.register_plugin
class RdGridContainerPlugin(CMSPluginBase):

    model = RdGridContainer
    name = 'Container'
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
    name = 'Layout'
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
    name = 'Cell'
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
    name = 'Icon'
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
class RdTabGroupPlugin(CMSPluginBase):

    model = RdTabGroup
    name = 'Group of tabs'
    module = 'Reddevil'
    render_template = 'rd_django/tab_group.html'
    allow_children = True
    child_classes = ['RdTabPlugin']

    def render(self, context, instance, placeholder):
        context['slidercolor'] = instance.slidercolor
        return super(RdTabGroupPlugin, self).render(
            context, instance, placeholder)

@plugin_pool.register_plugin
class RdTabPlugin(CMSPluginBase):

    model = RdTab
    name = 'Tab'
    module = 'Reddevil'
    render_template = 'rd_django/tab.html'
    require_parent = True
    allow_children = True

    # form = RdPersonForm

    def render(self, context, instance, placeholder):
        context['tabtitle'] = instance.tabtitle
        return super(RdTabPlugin, self).render(
            context, instance, placeholder)

@plugin_pool.register_plugin
class RdBoxPlugin(CMSPluginBase):

    model = RdBox
    name = 'Box'
    module = 'Reddevil'
    render_template = 'rd_django/box.html'
    allow_children = True

    # form = RdPersonForm

    def render(self, context, instance, placeholder):
        context['boxtitle'] = instance.boxtitle
        context['boxtitlecolor'] = instance.boxtitlecolor or 'black'
        context['boxbackgroundcolor'] = instance.boxbackgroundcolor or 'grey'
        return super(RdBoxPlugin, self).render(
            context, instance, placeholder)