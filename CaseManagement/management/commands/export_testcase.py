import datetime

import xlwt
# 导出Excel
from django.contrib import admin
from django.http import StreamingHttpResponse

filename=datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
class AdminReport(admin.ModelAdmin):
    # actions = ["saveexecl"]  # 自定义的action（导出到excel表格）
    # list_display = ("id", 'offer', 'day_time', 'idfa', 'submit_result_text', 'callback_result_text')  # 显示的列
    # search_fields = ('day_time', 'callback_result_text')  # 可以搜索的字段
    # date_hierarchy = 'day_time'  # 按照日期显示
    # list_filter = ('offer',)  # 过滤条件
    # list_per_page = 500  # 每页显示500条，太多了可能会出现服务器崩掉的情况

    def saveexecl(self, request, queryset):
        Begin = xlwt.Workbook()
        sheet = Begin.add_sheet("response")
        cols = 0
        for query in queryset:
            # you need write colms                     # 好像有个方法可以一次性写入所有列，记不清了，只能用这种简单的方法去实现
            sheet.write(cols, 1, str(query.idfa))  # 写入第一列
            sheet.write(cols, 2, str(query.day_time))  # 写入第二列
            sheet.write(cols, 3, str(query.keyword))  # 写入第三列
            cols += 1
        Begin.save("%s" % (filename))

        def file_iterator(filename, chuck_size=512):
            with open(filename, "rb") as f:
                while True:
                    c = f.read(chuck_size)
                    if c:
                        yield c
                    else:
                        break

        response = StreamingHttpResponse(file_iterator(filename))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="{}"'.format("result.xls")
        return response

    # saveexecl.short_description = "导出Excel"  # 按钮显示名字


# admin.site.register(Report, AdminReport)  # 注册到admin
