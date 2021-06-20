import csv
from django.core.management import BaseCommand
from CaseManagement.models import DB_testcase


# python manage.py  export_testcase --path D:\code\TestCaseManagement\CaseManagement\data\testcase.csv


class Command(BaseCommand):
    help = '从数据库中读取测试用例的列表，导出到Excel中'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)

    def handle(self, *args, **options):
        print("1111111")
        t=DB_testcase.objects.all()
        for i in t:
            print(i.t_purpose)
            print(i.t_id)
            print(i.t_id)
