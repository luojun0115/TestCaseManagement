from django.contrib import admin

# Register your models here.
from blog.models import Article, ArticleCategory


class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'publish_date')


admin.site.register(Article, BlogAdmin)
admin.site.register(ArticleCategory)
