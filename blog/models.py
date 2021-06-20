# from datetime import timezone

from django.db import models
from django.utils import timezone


class ArticleCategory(models.Model):
    title = models.CharField(max_length=100, blank=True)
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'tb_category'
        verbose_name = '类别管理'
        verbose_name_plural = verbose_name

# Create your models here.
class Article(models.Model):
    article_id = models.AutoField(primary_key=True)
    # 文章的标题
    title = models.TextField()

    # 文章的摘要
    brief_content = models.TextField()
    # 文章的内容
    content = models.TextField()

    # 文本的发布日期
    publish_date = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(ArticleCategory, on_delete=models.CASCADE)

    class Meta:
        db_table = 'db_article'
        verbose_name = u'博客网站'
        ordering = ['publish_date']
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title



