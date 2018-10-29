from django.db import models

# Create your models here.
from django.contrib.auth.models import User as Auser

from Business.models import Business
from Data.models import Data
from Tag.models import Function, Case, User


class SuiteName(models.Model):
    suitename = models.CharField(max_length=15, verbose_name="组件名称", unique=True, help_text="英文名称，以.robot为后缀名")
    function = models.ForeignKey(Function, verbose_name='功能模块')
    documentation = models.TextField(verbose_name="组件描述")
    del_flag = models.IntegerField(default=0, editable=False)

    class Meta:
        db_table = 'test_suite'
        verbose_name = "用例组件"
        verbose_name_plural = verbose_name
        ordering = ['suitename']

    def __str__(self):
        return self.suitename + '（' + self.function.tagName + '）'


class CaseBdd(models.Model):
    suite = models.ForeignKey(SuiteName, verbose_name='组件名称')
    name = models.CharField(max_length=20, verbose_name="用例名称", unique=True)
    tag = models.ManyToManyField(Case, verbose_name='用例标签', blank=True)
    isrun = models.CharField(max_length=10, verbose_name='是否执行', choices=(('Run', '执行'), ('NotRun', '不执行')),
                             default='Run')
    business = models.ManyToManyField(Business, through='CaseBddToBusiness', verbose_name='用例流程')
    documentation = models.TextField(verbose_name="用例描述", blank=True, null=True)
    sort = models.IntegerField(verbose_name="排序", default=999)
    date = models.DateField(auto_now=True)
    writer = models.ForeignKey(Auser, verbose_name="编写人", on_delete=models.CASCADE, editable=False)
    del_flag = models.IntegerField(default=0, editable=False)

    class Meta:
        db_table = 'case'
        verbose_name = "测试用例"
        verbose_name_plural = verbose_name
        ordering = ['suite', 'sort']

    def __str__(self):
        return self.name


class CaseBddToBusiness(models.Model):
    case = models.ForeignKey(CaseBdd, verbose_name='用例名称')
    bus = models.ForeignKey(Business, verbose_name='流程名称')
    user = models.ForeignKey(User, verbose_name='用例执行者')
    param = models.ManyToManyField(Data, verbose_name='用例参数', blank=True)
    sort = models.IntegerField(verbose_name="排序", default='1')
    del_flag = models.IntegerField(default=0, editable=False)

    class Meta:
        db_table = 'case_business'
        verbose_name = "用例流程设置"
        verbose_name_plural = verbose_name
        ordering = ['sort']

    def __str__(self):
        return self.case.name
