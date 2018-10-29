from django import forms
from django.contrib import admin

# Register your models here.
import xadmin
from Business.models import Business, BusinessToVariable
from Tag.models import Business as Tbus


class TagForm(forms.ModelForm):
    complete = forms.ModelMultipleChoiceField(
        queryset=Tbus.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        label="代码实现",
        help_text="*** 在编写实现代码前，都选对应标签，可以在前台初始化业务代码 ***",
        required=False)

    class Meta:
        model = Business
        # 规定哪些字段不想加入表单中
        exclude = []


class BusinessSetting(object):
    form = TagForm
    list_display = ('chinesename', 'name', 'variable', 'documentation')


class BTVSetting(object):
    list_display = ('busname', 'var', 'sort')


xadmin.site.register(Business, BusinessSetting)
xadmin.site.register(BusinessToVariable, BTVSetting)
