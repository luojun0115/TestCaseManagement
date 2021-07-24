import datetime

import xlwt
# ����Excel
from django.contrib import admin
from django.http import StreamingHttpResponse

filename=datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
class AdminReport(admin.ModelAdmin):
    # actions = ["saveexecl"]  # �Զ����action��������excel���
    # list_display = ("id", 'offer', 'day_time', 'idfa', 'submit_result_text', 'callback_result_text')  # ��ʾ����
    # search_fields = ('day_time', 'callback_result_text')  # �����������ֶ�
    # date_hierarchy = 'day_time'  # ����������ʾ
    # list_filter = ('offer',)  # ��������
    # list_per_page = 500  # ÿҳ��ʾ500����̫���˿��ܻ���ַ��������������

    def saveexecl(self, request, queryset):
        Begin = xlwt.Workbook()
        sheet = Begin.add_sheet("response")
        cols = 0
        for query in queryset:
            # you need write colms                     # �����и���������һ����д�������У��ǲ����ˣ�ֻ�������ּ򵥵ķ���ȥʵ��
            sheet.write(cols, 1, str(query.idfa))  # д���һ��
            sheet.write(cols, 2, str(query.day_time))  # д��ڶ���
            sheet.write(cols, 3, str(query.keyword))  # д�������
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

    # saveexecl.short_description = "����Excel"  # ��ť��ʾ����


# admin.site.register(Report, AdminReport)  # ע�ᵽadmin
