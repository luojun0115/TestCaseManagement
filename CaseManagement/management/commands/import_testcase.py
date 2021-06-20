import csv
from django.core.management import BaseCommand
from CaseManagement.models import DB_testcase


# 命令
# python manage.py  import_testcase --path python manage.py  import_testcase --path D:\code\TestCaseManagement\CaseManagement\data\testcase.csv
# python manage.py  import_testcase --path D:\code\TestCaseManagement\CaseManagement\data\testcase.csv

class Command(BaseCommand):
    help = '从一个csv文件的内容中读取测试用例的列表，导入到数据库中'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)

    def handle(self, *args, **options):
        path = options['path']
        with open(path, 'rt') as f:
            reader = csv.reader(f, dialect='excel')
            for row in reader:
                testcase = DB_testcase.objects.create(
                    # t_id=row[0], # 主键会自动添加
                    t_module=row[1],
                    t_priority=row[2],
                    t_purpose=row[3],
                    t_precondition=row[4],
                    t_steps=row[5],
                    t_expected_result=row[6],
                    t_actual_result=row[7],
                    t_remark=row[8],
                )
                print('导入完成。。。。')
            print('all testcase导入完成。。。。')
