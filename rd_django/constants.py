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



from django.utils.translation import ugettext_lazy as _


GRID_SIZE = 12

GRID_CELL_SIZES = [('','')] + [(str(i+1), str(i+1)) for i in range(GRID_SIZE)]

GRID_CONTAINER_CHOICES = (
    ('fixed', _('Fixed container')),
    ('fluid', _('Fluid container')),
)

GRID_LAYOUT_CHOICES = (
    ('horizontal', _('Horizontal layout')),
    ('vertical', _('Vertical layout')),
)

GRID_DISPLAYS = ['xs', 'sm', 'md', 'lg', 'xl']

GRID_GUTTER_CHOICES = (
    ('', _('no gutter')),
    ('xs', _('extra small gutter')),
    ('sm', _('small gutter')),
    ('md', _('medium gutter')),
    ('lg', _('large gutter')),
    ('xl', _('extra large gutter')),
)
