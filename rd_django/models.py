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

import collections

from django.db import models
from cms.models.pluginmodel import CMSPlugin


# vuetify container

class RdGridContainerConstants:

    CONTAINERS = (
        ('fixed', 'Fixed container'),
        ('fluid', 'Fluid container'),
    )
    GUTTERS = (
        ('', 'no gutter'),
        ('xs', 'extra small gutter'),
        ('sm', 'small gutter'),
        ('md', 'medium gutter'),
        ('lg', 'large gutter'),
        ('xl', 'extra large gutter'),
    )

class RdGridContainer(CMSPlugin):
    """
    a db model for a <v-container> element
    """

    container = models.CharField(
        verbose_name='Container type',
        choices=RdGridContainerConstants.CONTAINERS,
        default=RdGridContainerConstants.CONTAINERS[0][0],
        blank=True,
        max_length=20,
    )
    gutter = models.CharField(
        verbose_name='Gutter between cells',
        choices=RdGridContainerConstants.GUTTERS,
        default=RdGridContainerConstants.GUTTERS[0][0],
        max_length=3,
        blank=True,
    )

    def __str__(self):
        return str(self.pk)

    def get_short_description(self):
        text = ''
        for item in RdGridContainerConstants.CONTAINERS:
            if item[0] == self.container:
                text = item[1]
        gutter = ''
        if item[0] == self.container:
            for item in RdGridContainerConstants.GUTTERS:
                if item[0] == self.gutter:
                    gutter = item[1]
        return '({}, {})'.format(text, gutter)

# vuetify layout

class RdGridLayoutConstants:

    LAYOUTS = (
        ('horizontal', 'Horizontal layout'),
        ('vertical', 'Vertical layout'),
    )

class RdGridLayout(CMSPlugin):
    """
    a db model for a <v-layout> element
    """

    layout = models.CharField(
        verbose_name='direction',
        choices=RdGridLayoutConstants.LAYOUTS,
        default=RdGridLayoutConstants.LAYOUTS[0][0],
        max_length=20,
    )
    wrap = models.BooleanField(
        verbose_name='Wrap cells if width is exceeded',
        default=True,
    )

    def __str__(self):
        return str(self.pk)

    def get_short_description(self):
        text = []
        for item in RdGridLayoutConstants.LAYOUTS:
            if item[0] == self.layout:
                text.append(str(item[1]))
        if self.wrap:
            text.append(str('wrap'))
        return '({})'.format(', '.join(text))


# veutify flex

class RdGridCellConstants:

    SIZES = [('', '')] + [(str(i + 1), str(i + 1)) for i in range(12)]
    DISPLAYS = ['xs', 'sm', 'md', 'lg', 'xl']

class RdGridCell(CMSPlugin):
    """
    a db model for <v-flex> element
    """

    xs_size = models.CharField(
        verbose_name='width cell for extra small display',
        choices=RdGridCellConstants.SIZES,
        default='',
        blank=True,
        max_length=2,
    )
    sm_size = models.CharField(
        verbose_name='width cell for small display',
        choices=RdGridCellConstants.SIZES,
        default='',
        blank=True,
        max_length=2,
    )
    md_size = models.CharField(
        verbose_name='width cell medium display',
        choices=RdGridCellConstants.SIZES,
        default='',
        blank=True,
        max_length=2,
    )
    lg_size = models.CharField(
        verbose_name='width cell large display',
        choices=RdGridCellConstants.SIZES,
        default='',
        blank=True,
        max_length=2,
    )
    xl_size = models.CharField(
        verbose_name='width cell extra large display',
        choices=RdGridCellConstants.SIZES,
        default='',
        blank=True,
        max_length=2,
    )
    xs_offset = models.CharField(
        verbose_name='offset for extra small display',
        choices=RdGridCellConstants.SIZES,
        default='',
        blank=True,
        max_length=2,
    )
    sm_offset = models.CharField(
        verbose_name='offset for small display',
        choices=RdGridCellConstants.SIZES,
        default='',
        blank=True,
        max_length=2,
    )
    md_offset = models.CharField(
        verbose_name='offset medium display',
        choices=RdGridCellConstants.SIZES,
        default='',
        blank=True,
        max_length=2,
    )
    lg_offset = models.CharField(
        verbose_name='offset large display',
        choices=RdGridCellConstants.SIZES,
        default='',
        blank=True,
        max_length=2,
    )
    xl_offset = models.CharField(
        verbose_name='offset extra large display',
        choices=RdGridCellConstants.SIZES,
        default='',
        blank=True,
        max_length=2,
    )

    def __str__(self):
        return str(self.pk)

    def get_short_description(self):
        text = []
        for d in RdGridCellConstants.DISPLAYS:
            fieldsize = getattr(self, '{}_size'.format(d))
            if fieldsize:
                text.append('{}{}'.format(d, fieldsize))
        for d in RdGridCellConstants.DISPLAYS:
            fieldoffset = getattr(self, '{}_offset'.format(d))
            if fieldoffset:
                text.append('offset-{}{}'.format(d, fieldoffset))

# icon

class RdIconConstants:

    SIZES = (
        ('', 'standard'),
        ('small', 'small'),
        ('medium', 'medium'),
        ('large', 'large'),
        ('x-large', 'extra large'),
    )
    THEMES = (
        ('', 'standard'),
        ('dark', 'dark'),
        ('light', 'light'),
    )

class RdIcon(CMSPlugin):
    """
    a db model for a vuetify icon
    """

    icon = models.CharField(
        verbose_name='Icon',
        max_length=40,
    )
    size = models.CharField(
        verbose_name='size of icon',
        choices = RdIconConstants.SIZES,
        default='',
        blank=True,
        max_length=10,
    )
    color = models.CharField(
        verbose_name='Color',
        max_length=30,
        default='',
        blank=True,
    )
    theme = models.CharField(
        verbose_name='Theme',
        choices = RdIconConstants.THEMES,
        max_length=10,
        default='',
        blank=True,
    )
    additional_classes= models.CharField(
        verbose_name='Additional CSS classes (separated by a space)',
        max_length=255,
        default='',
        blank=True,
    )
    def __str__(self):
        return str(self.pk)

    def get_short_description(self):
        text = [self.icon]
        for sz in RdIconConstants.SIZES:
            if sz[0] == self.size:
                text.append(str(sz[1]))
        if self.color:
            text.append(self.color)
        if self.theme:
            text.append(self.theme)
        return ' '.join(text)


class RdTabGroup(CMSPlugin):
    """
    a db model for a group of tabs
    """
    slidercolor = models.CharField(
        verbose_name='Slider color',
        max_length=40,
        default='accent'
    )

class RdTab(CMSPlugin):
    """
    a db model for a tabular UI component inside a tabgroup
    """

    tabtitle = models.CharField(
        verbose_name='Title of the tab',
        max_length=40,
    )
    def __str__(self):
        return self.tabtitle

class RdBox(CMSPlugin):
    """
    a db model for a tabular UI component inside a tabgroup
    """

    boxtitle = models.CharField(
        verbose_name='Title of the box',
        max_length=40,
    )
    boxtitlecolor = models.CharField(
        verbose_name='Box title color',
        max_length=40,
        default='black'
    )
    boxbackgroundcolor = models.CharField(
        verbose_name='Box background color title',
        max_length=40,
        default='grey'
    )
    def __str__(self):
        return self.boxtitle
