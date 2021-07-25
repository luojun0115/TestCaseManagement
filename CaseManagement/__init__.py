# import csv
# import datetime
#
# from django.contrib import admin
#
# # Register your models here.
# from django.http import HttpResponse
# from import_export import resources
# from import_export.admin import ImportExportModelAdmin
#
# from CaseManagement.models import DB_testcase, DB_module, Article, ArticleCategory
#
# # exportable_fields = (
# #     't_module',
# #     't_priority',
# #     't_purpose',
# #     't_steps',
# #     't_precondition',
# #     't_expected_result',
# #     't_actual_result',
# #     't_remark',
# # )
#
#
# # def export_model_as_csv(modeladmin, request, queryset):
# #     response = HttpResponse(content_type='text/csv')
# #     response['Content-Disposition'] = 'attachment; filename=%s.csv' % (
# #         datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
# #     )
# #     response.charset = 'utf-8-sig'
# #     writer = csv.writer(response)
# #     writer.writerow(exportable_fields)
# #
# #     for obj in queryset:
# #         row = writer.writerow([getattr(obj, field) for field in exportable_fields])
# #     return response
#
#
# # 参考文章
# # https://blog.csdn.net/weixin_30539625/article/details/101325340
#
#
# # export_model_as_csv.short_description = '导出到CSV_我去挣钱'
#
#
# # class TestCaseAdmin(admin.ModelAdmin):
# #     actions = [export_model_as_csv, ]
# #     list_display = [
# #         't_module',
# #         't_priority',
# #         't_purpose',
# #         't_steps',
# #         't_precondition',
# #         't_expected_result',
# #         't_actual_result',
# #         't_remark',
# #     ]
#
#
# class CaseResource(resources.ModelResource):
#     class Meta:
#         model = DB_testcase
#         export_order = ('t_priority', 't_precondition')
#
#         # skip_unchanged = True
#         # report_skipped = True
#         exclude = ('id',)
#         # export_order = ('edx_id', 'edx_email')
#         import_id_fields = (
#                             # 't_id',
#                             't_module',
#                             't_priority',
#                             't_purpose',
#                             't_steps',
#                             't_precondition',
#                             't_expected_result',
#                             't_actual_result',
#                             't_remark',
#                             )
#         export_order =(
#                             # 't_id',
#                             't_module',
#                             't_priority',
#                             't_purpose',
#                             't_steps',
#                             't_precondition',
#                             't_expected_result',
#                             't_actual_result',
#                             't_remark',
#                             )
#
#
# # @admin.register(DB_testcase)
# class CaseAdmin(ImportExportModelAdmin):
#     list_display = [
#         't_module',
#         't_priority',
#         't_purpose',
#         't_steps',
#         't_precondition',
#         't_expected_result',
#         't_actual_result',
#         't_remark',
#     ]
#
#     resource_class = CaseResource
#
#
# # admin.site.register(DB_testcase, TestCaseAdmin)
# admin.site.register(DB_testcase, CaseAdmin)
# admin.site.register(DB_module)
# admin.site.register(Article)
# admin.site.register(ArticleCategory)
