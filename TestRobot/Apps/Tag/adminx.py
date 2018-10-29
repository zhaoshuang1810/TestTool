from django.contrib import admin

# Register your models here.
import xadmin
from Tag.models import User, Case, Function, Business


class UserSetting(object):
    list_display = ('chinesename', 'user', 'userid', 'reqchannel')
    # 可点击链接字段
    list_display_links = ('user',)
    # 每页显示多少条数据
    list_per_page = 10


class CaseSetting(object):
    list_display = ('tagName', 'tag', 'documentation')
    list_per_page = 10


class BusSetting(object):
    list_display = ('tagName', 'tag', 'documentation')
    list_per_page = 10


class FunctionSetting(object):
    list_display = ('tagName', 'tag', 'documentation')
    list_per_page = 10


xadmin.site.register(User, UserSetting)
xadmin.site.register(Case, CaseSetting)
xadmin.site.register(Business, BusSetting)
xadmin.site.register(Function, FunctionSetting)
