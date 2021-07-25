from django.db import models
# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.utils import timezone


class ArticleCategory(models.Model):
    """
    文章分类
    """
    # 分类标题
    title = models.CharField(max_length=100, blank=True)
    # 分类的创建时间
    created = models.DateTimeField(default=timezone.now)

    # admin站点显示，调试查看对象方便
    def __str__(self):
        return self.title

    class Meta:
        db_table = 'tb_category'  # 修改表名
        verbose_name = '类别管理'  # admin站点显示
        verbose_name_plural = verbose_name



class Article(models.Model):
    # 标题
    title = models.CharField(max_length=20, blank=True)
    # 分类
    category = models.ForeignKey(ArticleCategory, null=True, blank=True, on_delete=models.CASCADE,
                                 related_name='article')
    # 文章正文
    content = models.TextField()

    created = models.DateTimeField(default=timezone.now)
    # 文章的修改时间
    updated = models.DateTimeField(auto_now=True)

    # 修改表名以及admin展示的配置信息等
    class Meta:
        db_table = 'tb_article'
        ordering = ('created',)
        verbose_name = '文章管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class DB_module(models.Model):
    t_module_name = models.CharField(max_length=100, verbose_name="模块名称")
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.t_module_name

    class Meta:
        db_table = u'db_module'
        verbose_name = '模块名称'
        verbose_name_plural = verbose_name


# Create your models here.
class DB_testcase(models.Model):
    """
    测试用例
    """
    # t_id = models.AutoField(primary_key=True, verbose_name="用例编号")  # 用例编号
    t_priority = models.CharField(max_length=100, verbose_name="优先级")  # 优先级
    t_purpose = models.CharField(max_length=100, verbose_name="测试目的")  # 测试目的
    t_precondition = models.CharField(max_length=100, verbose_name="前置条件")  # 前置条件
    t_steps = models.CharField(max_length=100, verbose_name="测试步骤")  # 测试步骤
    # t_data=models.CharField(max_length=100,null=True,verbose_name=" 数据准备")#  数据准备
    t_expected_result = models.CharField(max_length=100, verbose_name="预期结果")  # 预期结果
    t_actual_result = models.CharField(max_length=100, verbose_name="实际结果")  # 实际结果
    # t_version_number=models.CharField(max_length=100,null=True)# 测试版本
    t_remark = models.CharField(max_length=100, null=True, blank=True, verbose_name="备注")  # 备注
    t_module = models.ForeignKey(DB_module, verbose_name="模块名称", on_delete=models.CASCADE,null=True, blank=True)  # 所属模块

    class Meta:
        db_table = u'db_testcase'
        verbose_name = u'测试用例'
        # ordering = ['t_id']
        ordering = ['t_priority']
        verbose_name_plural = u'测试用例'

    def __str__(self):
        # 测试目的
        return self.t_purpose
