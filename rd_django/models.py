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
from django.utils.translation import ugettext_lazy as _
from cms.models.pluginmodel import CMSPlugin


# vuetify container

class RdGridContainerConstants:

    CONTAINERS = (
        ('fixed', _('Fixed container')),
        ('fluid', _('Fluid container')),
    )
    GUTTERS = (
        ('', _('no gutter')),
        ('xs', _('extra small gutter')),
        ('sm', _('small gutter')),
        ('md', _('medium gutter')),
        ('lg', _('large gutter')),
        ('xl', _('extra large gutter')),
    )

class RdGridContainer(CMSPlugin):
    """
    a db model for a <v-container> element
    """

    container = models.CharField(
        verbose_name=_('Container type'),
        choices=RdGridContainerConstants.CONTAINERS,
        default=RdGridContainerConstants.CONTAINERS[0][0],
        blank=True,
        max_length=20,
    )
    gutter = models.CharField(
        verbose_name=_('Gutter between cells'),
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
        ('horizontal', _('Horizontal layout')),
        ('vertical', _('Vertical layout')),
    )

class RdGridLayout(CMSPlugin):
    """
    a db model for a <v-layout> element
    """

    layout = models.CharField(
        verbose_name=_('direction'),
        choices=RdGridLayoutConstants.LAYOUTS,
        default=RdGridLayoutConstants.LAYOUTS[0][0],
        max_length=20,
    )
    wrap = models.BooleanField(
        verbose_name=_('Wrap cells if width is exceeded'),
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
            text.append(str(_('wrap')))
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
        verbose_name=_('width cell for extra small display'),
        choices=RdGridCellConstants.SIZES,
        default='',
        blank=True,
        max_length=2,
    )
    sm_size = models.CharField(
        verbose_name=_('width cell for small display'),
        choices=RdGridCellConstants.SIZES,
        default='',
        blank=True,
        max_length=2,
    )
    md_size = models.CharField(
        verbose_name=_('width cell medium display'),
        choices=RdGridCellConstants.SIZES,
        default='',
        blank=True,
        max_length=2,
    )
    lg_size = models.CharField(
        verbose_name=_('width cell large display'),
        choices=RdGridCellConstants.SIZES,
        default='',
        blank=True,
        max_length=2,
    )
    xl_size = models.CharField(
        verbose_name=_('width cell extra large display'),
        choices=RdGridCellConstants.SIZES,
        default='',
        blank=True,
        max_length=2,
    )
    xs_offset = models.CharField(
        verbose_name=_('offset for extra small display'),
        choices=RdGridCellConstants.SIZES,
        default='',
        blank=True,
        max_length=2,
    )
    sm_offset = models.CharField(
        verbose_name=_('offset for small display'),
        choices=RdGridCellConstants.SIZES,
        default='',
        blank=True,
        max_length=2,
    )
    md_offset = models.CharField(
        verbose_name=_('offset medium display'),
        choices=RdGridCellConstants.SIZES,
        default='',
        blank=True,
        max_length=2,
    )
    lg_offset = models.CharField(
        verbose_name=_('offset large display'),
        choices=RdGridCellConstants.SIZES,
        default='',
        blank=True,
        max_length=2,
    )
    xl_offset = models.CharField(
        verbose_name=_('offset extra large display'),
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
        ('', _('standard')),
        ('small', _('small')),
        ('medium', _('medium')),
        ('large', _('large')),
        ('x-large', _('extra large')),
    )
    THEMES = (
        ('', _('standard')),
        ('dark', _('dark')),
        ('light', _('light')),
    )

class RdIcon(CMSPlugin):
    """
    a db model for a vuetify icon
    """

    icon = models.CharField(
        verbose_name=_('Icon'),
        max_length=40,
    )
    size = models.CharField(
        verbose_name=_('size of icon'),
        choices = RdIconConstants.SIZES,
        default='',
        blank=True,
        max_length=10,
    )
    color = models.CharField(
        verbose_name=_('Color'),
        max_length=30,
        default='',
        blank=True,
    )
    theme = models.CharField(
        verbose_name=_('Theme'),
        choices = RdIconConstants.THEMES,
        max_length=10,
        default='',
        blank=True,
    )
    additional_classes= models.CharField(
        verbose_name=_('Additional CSS classes (separated by a space)'),
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


class RdPersonGroup(CMSPlugin):
    """
    a db model for a list of person in a group
    """
    group = models.CharField(
        verbose_name=_('Group'),
        max_length=39,
    )
    def __str__(self):
        return self.group

    def get_short_description(self):
        return self.group

class RdPerson(CMSPlugin):
    """
    a db model for a vuetify person
    """

    idbel = models.CharField(
        verbose_name=_('ID number RBCF'),
        max_length=10,
    )
    def __str__(self):
        return self.idbel

    def get_short_description(self):
        return self.idbel


class RdTabGroup(CMSPlugin):
    """
    a db model for a group of tabs
    """
    slidercolor = models.CharField(
        verbose_name=_('Slider color'),
        max_length=40,
        default='accent'
    )

class RdTab(CMSPlugin):
    """
    a db model for a tabular UI component inside a tabgroup
    """

    tabtitle = models.CharField(
        verbose_name=_('Title of the tab'),
        max_length=40,
    )
    def __str__(self):
        return self.tabtitle

