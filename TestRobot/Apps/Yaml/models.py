from django.db import models


# Create your models here.

class File(models.Model):
    name = models.CharField(max_length=30, verbose_name='接口文件名', unique=True)
    host = models.CharField(max_length=30, verbose_name='主机地址', blank=True, null=True)
    basepath = models.CharField(max_length=30, verbose_name='基础地址', blank=True, null=True)
    date = models.DateField(auto_now=True)
    del_flag = models.IntegerField(default=0, editable=False)

    class Meta:
        db_table = 'yaml_file'
        verbose_name = "接口文档"
        verbose_name_plural = verbose_name
        ordering = ['name']

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=30, verbose_name='标签名称')
    description = models.CharField(max_length=30, verbose_name='标签描述', blank=True, null=True)
    file = models.ForeignKey(File, verbose_name="所属接口文件")
    del_flag = models.IntegerField(default=0, editable=False)

    class Meta:
        db_table = 'yaml_tag'
        verbose_name = "接口标签"
        verbose_name_plural = verbose_name
        unique_together = (('name', 'file'))
        ordering = ['file']

    def __str__(self):
        return self.name + '(' + self.file.name + ')'


class Path(models.Model):
    file = models.ForeignKey(File, verbose_name="所属接口文件")
    path = models.CharField(max_length=60, verbose_name='接口路径')
    modelist = (
        ('get', "GET"),
        ('post', 'POST'),
        ('put', 'PUT')
    )
    mode = models.CharField(max_length=10, verbose_name='请求方式', choices=modelist)
    tag = models.ForeignKey(Tag, verbose_name='接口标签')
    summary = models.CharField(max_length=100, verbose_name='接口简介')
    description = models.TextField(verbose_name='接口描述', blank=True, null=True)
    resp = models.TextField(verbose_name='接口返回值', blank=True, null=True)
    date = models.DateField(auto_now=True)
    del_flag = models.IntegerField(default=0, editable=False)

    class Meta:
        db_table = 'yaml_path'
        verbose_name = "接口路径"
        verbose_name_plural = verbose_name
        unique_together = (('path', 'mode'))
        ordering = ['path']

    def __str__(self):
        return self.path + "--" + self.mode


class Param(models.Model):
    path = models.ForeignKey(Path, verbose_name='接口')
    name = models.CharField(max_length=30, verbose_name='参数名称')
    value = models.TextField(verbose_name='参数值', blank=True, null=True)
    methodlist = (
        ('query', 'query'),
        ('path', 'path'),
        ('body', 'body'),
        ('header', 'header')
    )
    method = models.CharField(max_length=30, verbose_name='参数属性', choices=methodlist)
    typelist = (
        ('1', "字符型"),
        ('0', "整数型"),
        ('2', "布尔型"),
        ('3', "body参数"),
        ('4', "其他类型"),

    )
    ptype = models.CharField(max_length=30, verbose_name='参数类型', choices=typelist)
    required = models.IntegerField(verbose_name='是否必要', choices=((1, '必要'), (0, '不必要')), default=1)
    description = models.TextField(verbose_name='参数描述', blank=True, null=True)
    del_flag = models.IntegerField(default=0, editable=False)

    class Meta:
        db_table = 'yaml_param'
        verbose_name = "接口参数"
        verbose_name_plural = verbose_name
        ordering = ['path']

    def __str__(self):
        return self.path.path + "--" + self.path.mode + " : " + self.name
