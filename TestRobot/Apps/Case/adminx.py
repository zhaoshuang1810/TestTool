from django import forms
from django.contrib import admin

# Register your models here.

# class BaseSetting(object):
#     enable_themes = True  # 打开主题功能
#     use_bootswatch = True  #
import xadmin
from Case.models import SuiteName, CaseBdd, CaseBddToBusiness
from Config.project import projectName
from Tag.models import Case
from xadmin import views
from xadmin.layout import Fieldset, Row, Col


class GlobalSetting(object):
    # 设置base_site.html的Title
    site_title = projectName
    # 设置base_site.html的Footer
    site_footer = '自动化测试工具'
    menu_style = "accordion"


# xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSetting)


class SuiteNameSetting(object):
    list_display = ('suitename', 'documentation', 'function')


class TagForm(forms.ModelForm):
    tag = forms.ModelMultipleChoiceField(
        queryset=Case.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        label="用例标签",
        required=False)

    class Meta:
        model = CaseBdd
        # 规定哪些字段不想加入表单中
        exclude = []


class CaseBddSetting(object):
    form = TagForm

    # 保存时，保存当前登录人
    def save_models(self):
        self.new_obj.writer = self.request.user
        super().save_models()

    form_layout = (
        Fieldset(u'用例信息',
                 Row('name', 'suite'),
                 Row('documentation', ),
                 css_class='unsort no_title',
                 ),
    )

    list_display = ('suite', 'name', 'sort','documentation', 'writer')
    # style_fields = {'tag': 'm2m_transfer'}
    list_display_links = ('name',)


class CaseBddBusSetting(object):
    list_display = ('case', 'bus', 'user', 'param', 'sort')
    # 多对多，选框美化
    style_fields = {'param': 'm2m_transfer'}


xadmin.site.register(SuiteName, SuiteNameSetting)
xadmin.site.register(CaseBdd, CaseBddSetting)
xadmin.site.register(CaseBddToBusiness, CaseBddBusSetting)
