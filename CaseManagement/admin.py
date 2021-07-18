import csv
import datetime

from django.contrib import admin

# Register your models here.
from django.http import HttpResponse

from CaseManagement.models import DB_testcase, DB_module,Article,ArticleCategory

exportable_fields = (
    't_module',
    't_priority',
    't_purpose',
    't_steps',
    't_precondition',
    't_expected_result',
    't_actual_result',
    't_remark',
)


def export_model_as_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=%s.csv' % (
        datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    )
    response.charset = 'utf-8-sig'
    writer = csv.writer(response)
    writer.writerow(exportable_fields)

    for obj in queryset:
        row = writer.writerow([getattr(obj, field) for field in exportable_fields])
    return response


# 参考文章
# https://blog.csdn.net/weixin_30539625/article/details/101325340


export_model_as_csv.short_description = '测试数据导出到CSV_我去挣钱'


class TestCaseAdmin(admin.ModelAdmin):
    actions = [export_model_as_csv, ]
    list_display = [
        't_module',
        't_priority',
        't_purpose',
        't_steps',
        't_precondition',
        't_expected_result',
        't_actual_result',
        't_remark',
    ]


admin.site.register(DB_testcase, TestCaseAdmin)
admin.site.register(DB_module)
admin.site.register(Article)
admin.site.register(ArticleCategory)


