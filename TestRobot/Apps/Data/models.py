from django.db import models


# Create your models here.


class Variable(models.Model):
    name = models.CharField(max_length=20, verbose_name="变量名称", unique=True)
    documentation = models.TextField(verbose_name="变量描述")
    del_flag = models.IntegerField(default=0, editable=False)

    class Meta:
        db_table = 'variable'
        verbose_name = "变量名库"
        verbose_name_plural = verbose_name
        ordering = ['name']

    def __str__(self):
        return self.name


class Data(models.Model):
    variable = models.ForeignKey(Variable, verbose_name='变量名称')
    value = models.CharField(max_length=100, verbose_name="变量值", help_text="英文逗号分隔代表数组")
    documentation = models.TextField(verbose_name="变量描述",blank=True,null=True)
    del_flag = models.IntegerField(default=0, editable=False)

    class Meta:
        db_table = 'data'
        verbose_name = "变量赋值"
        verbose_name_plural = verbose_name
        unique_together = (('variable', 'value'),)
        ordering = ['variable']

    def __str__(self):
        return self.variable.name + '(' + self.value + ')'

