from django.contrib import admin

# Register your models here.
import xadmin
from Data.models import Variable, Data


class VariableSetting(object):
    list_display = ('name', 'documentation')


class DataSetting(object):
    list_display = ('variable', 'value', 'documentation')


xadmin.site.register(Variable, VariableSetting)
xadmin.site.register(Data, DataSetting)