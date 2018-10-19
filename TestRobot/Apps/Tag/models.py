from django.db import models
from django.contrib.auth.models import User as Auser


# Create your models here.
class User(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Auser, verbose_name="英文名称")
    chinesename = models.CharField(max_length=20, verbose_name="中文名称", blank=True, null=True)
    reqchannel = models.CharField(max_length=20, choices=(("MASTER", "轻题库"), ("MANGO_ACCOUNTING", "芒果会计")),
                                  verbose_name="用户渠道")
    token = models.TextField(verbose_name="用户TOKEN")
    udid = models.CharField(max_length=20, verbose_name='设备id', blank=True, null=True)
    url = models.CharField(max_length=20, verbose_name='服务器地址', blank=True, null=True)
    date = models.DateField(auto_now=True)
    del_flag = models.IntegerField(default=0, editable=False)

    class Meta:
        verbose_name = "用户标签"
        verbose_name_plural = verbose_name
        unique_together = (("user", "reqchannel"),)
        ordering = ['user']

    def __str__(self):
        return self.user + '(' + self.reqchannel + ')'


class Case(models.Model):
    id = models.AutoField(primary_key=True)
    tag = models.CharField(max_length=20, verbose_name="英文名称", unique=True)
    tagName = models.CharField(max_length=20, verbose_name="中文名称", unique=True)
    documentation = models.TextField(verbose_name="标签描述")
    del_flag = models.IntegerField(default=0, editable=False)

    class Meta:
        verbose_name = "用例标签"
        verbose_name_plural = verbose_name
        ordering = ['tag']

    def __str__(self):
        return self.tag + '(' + self.tagName + ')'


class Function(models.Model):
    id = models.AutoField(primary_key=True)
    tag = models.CharField(max_length=20, verbose_name="英文名称", unique=True)
    tagName = models.CharField(max_length=20, verbose_name="中文名称", unique=True)
    documentation = models.TextField(verbose_name="标签描述")
    del_flag = models.IntegerField(default=0, editable=False)

    class Meta:
        verbose_name = "功能标签"
        verbose_name_plural = verbose_name
        ordering = ['tag']

    def __str__(self):
        return self.tag + '(' + self.tagName + ')'


class FunctionChild(models.Model):
    id = models.AutoField(primary_key=True)
    tag = models.CharField(max_length=20, verbose_name="英文名称", unique=True)
    tagName = models.CharField(max_length=20, verbose_name="中文名称", unique=True)
    documentation = models.TextField(verbose_name="标签描述")
    del_flag = models.IntegerField(default=0, editable=False)

    class Meta:
        verbose_name = "二级功能标签"
        verbose_name_plural = verbose_name
        ordering = ['tag']

    def __str__(self):
        return self.tag + '(二级功能：' + self.tagName + ')'
