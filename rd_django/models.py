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

from django.db import models
from django.utils.translation import ugettext_lazy as _
from cms.models.pluginmodel import CMSPlugin

# translations

class RdTranslationAvailable(CMSPlugin):
    nl = models.BooleanField(default=False, verbose_name=_('Dutch version available'))
    fr = models.BooleanField(default=False, verbose_name=_('French version available'))
    de = models.BooleanField(default=False, verbose_name=_('German version available'))
    en = models.BooleanField(default=False, verbose_name=_('English version available'))

# grid

from .constants import (
    GRID_CELL_SIZES,
    GRID_CONTAINER_CHOICES,
    GRID_DISPLAYS,
    GRID_LAYOUT_CHOICES,
    GRID_GUTTER_CHOICES,
)

class RdGridContainer(CMSPlugin):
    container = models.CharField(
        verbose_name=_('Container type'),
        choices=GRID_CONTAINER_CHOICES,
        default=GRID_CONTAINER_CHOICES[0][0],
        blank=True,
        max_length=20,
    )
    gutter = models.CharField(
        verbose_name=_('Gutter between cells'),
        choices=GRID_GUTTER_CHOICES,
        default=GRID_GUTTER_CHOICES[0][0],
        max_length=3,
        blank=True,
    )

    def __str__(self):
        return str(self.pk)

    def get_short_description(self):
        text = ''
        for item in GRID_CONTAINER_CHOICES:
            if item[0] == self.container:
                text = item[1]
        gutter = ''
        if item[0] == self.container:
            for item in GRID_GUTTER_CHOICES:
                if item[0] == self.gutter:
                    gutter = item[1]
        return '({}, {})'.format(text, gutter)

class RdGridLayout(CMSPlugin):
    layout = models.CharField(
        verbose_name=_('direction'),
        choices=GRID_LAYOUT_CHOICES,
        default=GRID_LAYOUT_CHOICES[0][0],
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
        for item in GRID_LAYOUT_CHOICES:
            if item[0] == self.layout:
                text.append(str(item[1]))
        if self.wrap:
            text.append(str(_('wrap')))
        return '({})'.format(', '.join(text))

class RdGridCell(CMSPlugin):
    xs_size = models.CharField(
        verbose_name=_('width cell for extra small display'),
        choices=GRID_CELL_SIZES,
        default='',
        blank=True,
        max_length=2,
    )
    sm_size = models.CharField(
        verbose_name=_('width cell for small display'),
        choices=GRID_CELL_SIZES,
        default='',
        blank=True,
        max_length=2,
    )
    md_size = models.CharField(
        verbose_name=_('width cell medium display'),
        choices=GRID_CELL_SIZES,
        default='',
        blank=True,
        max_length=2,
    )
    lg_size = models.CharField(
        verbose_name=_('width cell large display'),
        choices=GRID_CELL_SIZES,
        default='',
        blank=True,
        max_length=2,
    )
    xl_size = models.CharField(
        verbose_name=_('width cell extra large display'),
        choices=GRID_CELL_SIZES,
        default='',
        blank=True,
        max_length=2,
    )
    xs_offset = models.CharField(
        verbose_name=_('offset for extra small display'),
        choices=GRID_CELL_SIZES,
        default='',
        blank=True,
        max_length=2,
    )
    sm_offset = models.CharField(
        verbose_name=_('offset for small display'),
        choices=GRID_CELL_SIZES,
        default='',
        blank=True,
        max_length=2,
    )
    md_offset = models.CharField(
        verbose_name=_('offset medium display'),
        choices=GRID_CELL_SIZES,
        default='',
        blank=True,
        max_length=2,
    )
    lg_offset = models.CharField(
        verbose_name=_('offset large display'),
        choices=GRID_CELL_SIZES,
        default='',
        blank=True,
        max_length=2,
    )
    xl_offset = models.CharField(
        verbose_name=_('offset extra large display'),
        choices=GRID_CELL_SIZES,
        default='',
        blank=True,
        max_length=2,
    )

    def __str__(self):
        return str(self.pk)

    def get_short_description(self):
        text = []
        for d in GRID_DISPLAYS:
            fieldsize = getattr(self, '{}_size'.format(d))
            if fieldsize:
                text.append('{}{}'.format(d, fieldsize))
        for d in GRID_DISPLAYS:
            fieldoffset = getattr(self, '{}_offset'.format(d))
            if fieldoffset:
                text.append('offset-{}{}'.format(d, fieldoffset))
