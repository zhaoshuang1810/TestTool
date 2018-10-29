from django.db import models

# Create your models here.
from Data.models import Variable
from Tag.models import Function, Business as Tbus


class Business(models.Model):
    fun = models.ForeignKey(Function, verbose_name='所属功能')
    chinesename = models.CharField(max_length=60, verbose_name='业务名称', unique=True)
    name = models.CharField(max_length=30, verbose_name='英文名称', unique=True)
    complete = models.ManyToManyField(Tbus, verbose_name='代码实现', blank=True)
    variable = models.ManyToManyField(Variable, through='BusinessToVariable', verbose_name='变量名称')
    documentation = models.TextField(verbose_name="业务描述")
    del_flag = models.IntegerField(default=0, editable=False)

    class Meta:
        db_table = 'business'
        verbose_name = "业务流程"
        verbose_name_plural = verbose_name
        ordering = ['chinesename']

    def __str__(self):
        variables = ""
        if self.variable.all():
            variables = "(" + ",".join([v.name for v in self.variable.all()]) + ")"
        return self.chinesename + variables


class BusinessToVariable(models.Model):
    bus = models.ForeignKey(Business, verbose_name='业务名称')
    var = models.ForeignKey(Variable, verbose_name='变量名称')
    sort = models.IntegerField(verbose_name='排序', default=1)
    del_flag = models.IntegerField(default=0, editable=False)

    def busname(self):
        return self.bus.chinesename

    class Meta:
        db_table = 'business_variable'
        verbose_name = "业务形参"
        verbose_name_plural = verbose_name
        ordering = ['sort']

    def __str__(self):
        return self.bus.chinesename + self.var.name
