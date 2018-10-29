from django.contrib import admin

# Register your models here.
import xadmin
from Yaml.models import File, Param, Path, Tag
from xadmin.layout import Fieldset, Row


class FileSetting(object):
    list_display = ('name', 'host', 'basepath')
    list_per_page = 10


class TagSetting(object):
    list_display = ('name', 'description', 'file')
    list_per_page = 10


class PathSetting(object):
    list_display = ('path', 'mode', 'tag', 'summary')
    list_per_page = 10


class ParamSetting(object):
    list_display = ('path', 'name', 'method', 'required', 'description')
    form_layout = (
        Fieldset(u'用例信息',
                 Row('path', ),
                 Row('name', 'method'),
                 Row('ptype', 'required'),
                 Row('value', ),
                 css_class='unsort no_title',
                 ),
    )
    list_per_page = 10


xadmin.site.register(File, FileSetting)
xadmin.site.register(Tag, TagSetting)
xadmin.site.register(Path, PathSetting)
xadmin.site.register(Param, ParamSetting)
