# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
import xadmin
from Config.project import projectName
from .models import User, Case, Function, FunctionChild
from xadmin import views
from xadmin.layout import Fieldset, Row


class GlobalSetting(object):
    # 设置base_site.html的Title
    site_title = projectName
    # 设置base_site.html的Footer
    site_footer = '自动化测试工具'
    # menu_style = "accordion"


xadmin.site.register(views.CommAdminView, GlobalSetting)


class UserSetting(object):
    pass


xadmin.site.register(User, UserSetting)
