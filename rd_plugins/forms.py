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



from django.forms import models, IntegerField, BooleanField
from django.utils.translation import ugettext_lazy as _

from .constants import GRID_SIZE
from .models import RdGridRow, RdGridColumn

class RdGridRowForm(models.ModelForm):
    create = IntegerField(
        label=_('Create columns'),
        help_text=_('Number of columns to create when saving.'),
        required=False,
        min_value=0,
        max_value=GRID_SIZE,
    )

    class Meta:
        model = RdGridRow
        fields = '__all__'


# class Bootstrap4GridColumnBaseForm(models.ModelForm):
#     class Meta:
#         model = RdGridColumn
#         fields = '__all__'
#
#
# # convert regular text type fields to number
# extra_fields_column = {}
# for size in DEVICE_SIZES:
#     extra_fields_column['{}_col'.format(size)] = IntegerField(
#         label='col-{}'.format(size),
#         required=False,
#         min_value=1,
#         max_value=GRID_SIZE,
#     )
#     extra_fields_column['{}_order'.format(size)] = IntegerField(
#         label='order-{}'.format(size),
#         required=False,
#         min_value=1,
#         max_value=GRID_SIZE,
#     )
#     extra_fields_column['{}_ml'.format(size)] = BooleanField(
#         label='ml-{}-auto'.format(size),
#         required=False,
#     )
#     extra_fields_column['{}_mr'.format(size)] = BooleanField(
#         label='mr-{}-auto'.format(size),
#         required=False,
#     )
#
# Bootstrap4GridColumnForm = type(
#     str('Bootstrap4GridColumnBaseForm'),
#     (Bootstrap4GridColumnBaseForm,),
#     extra_fields_column,
# )
