# -*- coding: utf-8 -*-
import csv
import datetime
import json
import os
import re
import time
from sqlite3 import DatabaseError

import xlrd
import xlwt
from django.contrib import admin
from django.core.paginator import Paginator
from django.http import HttpResponseBadRequest, HttpResponseNotFound, HttpResponse, JsonResponse, HttpResponseRedirect, \
    StreamingHttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

# from CaseManagement.management.commands.export_testcase import AdminReport
from django_redis import get_redis_connection

from CaseManagement.models import DB_testcase, DB_module, Article, ArticleCategory, User
from CaseManagement.utils.response_code import RETCODE
from TestCaseManagement import settings
from TestCaseManagement.settings import logger
from libs.captcha.captcha import captcha
from libs.yuntongxun.sms import CCP

filename = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')


## 获取短信验证码
def smscode(request):
    mobile = request.GET.get('mobile')
    image_code = request.GET.get('image_code')
    uuid = request.GET.get('uuid')
    # 验证下参数是否齐全
    if not all([mobile, image_code, uuid]):
        return JsonResponse({'code': RETCODE.NECESSARYPARAMERR, 'errmsg': '缺少必要的参数'})
    # 从redis中获取图片验证码
    redis_conn = get_redis_connection('default')
    real_image_code = redis_conn.get('img:%s' % uuid)
    # 判断验证码是否存在
    if not real_image_code:
        return JsonResponse({'code': RETCODE.IMAGECODEERR, 'errmsg': '验证码不存在'})
    # 防止验证码多次使用，故删除
    try:
        redis_conn.delete('img:%s' % uuid)
    except Exception as e:
        logger.error(e)
    # print(type(real_image_code)) # redis中存储的是byte类型
    # 验证码是否一致
    if (real_image_code).decode().upper() != (str(image_code)).upper():
        return JsonResponse({'code': RETCODE.IMAGECODEERR, 'errmsg': '验证码不一致'})

    # 发送短信
    import random
    numbers = random.randint(111111, 999999)
    redis_conn.setex('sms:%s' % mobile, 60, numbers)
    print(numbers)
    # 5.发送短信
    # 参数1： 测试手机号
    # 参数2：模板内容列表： {1} 短信验证码   {2} 分钟有效
    # 参数3：模板 免费开发测试使用的模板ID为1
    # Rr = CCP().send_template_sms(mobile, [numbers, 5], 1)
    # print(Rr)
    # 6.返回响应
    return JsonResponse({'code': RETCODE.OK, 'errmsg': '短信发送成功'})


##图片验证码
def imagecode(request):
    # 获取uuid
    uuid = request.GET.get('uuid')

    if uuid is None:
        return HttpResponseBadRequest('没有传递uuid')
        # 3.通过调用captcha 来生成图片验证码（图片二进制和图片内容）
    text, image = captcha.generate_captcha()
    # 4.将 图片内容保存到redis中
    #     uuid作为一个key， 图片内容作为一个value 同时我们还需要设置一个实效
    redis_conn = get_redis_connection('default')
    # key 设置为 uuid
    # value  text
    redis_conn.setex('img:%s' % uuid, 60, text)
    # 5.返回图片二进制
    return HttpResponse(image, content_type='image/jpeg')


# 注册
def register(request):
    if str(request.method).upper() =='GET':
        return render(request, 'templates/register.html')
    if str(request.method).upper() == 'POST':
        # 获取必须传的参数
        mobile = request.POST.get('mobile')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        smscode = request.POST.get('sms_code')

        # 验证必填参数是否齐全
        if not all([mobile, password, password2, smscode]):
            return HttpResponseBadRequest('缺少必传参数')

        if password != password2:
            return HttpResponseBadRequest('缺少必传参数')
        # 判断一下手机号是否重复了
        count = User.objects.filter(mobile=mobile).count()
        if count != 0:
            return HttpResponseBadRequest('手机号码重复！')

        # 验证手机号是否合法，否则无法发送短信
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return HttpResponseBadRequest('请输入正确的手机号码')

        #验证密码是否是否符合要求
        if not re.match(r'^[0-9A-Za-z]{8,20}$', password):
            return HttpResponseBadRequest('请输入8-20位的密码')

        # 验证短信验证码
        redis_conn = get_redis_connection('default')
        sms_code_server = redis_conn.get('sms:%s' % mobile)
        if sms_code_server is None:
            return HttpResponseBadRequest('短信验证码已过期')
        if smscode != sms_code_server.decode():
            return HttpResponseBadRequest('短信验证码错误')

        # 保存注册数据
        try:
            user = User.objects.create_user(username=mobile, mobile=mobile, password=password)
        except DatabaseError:
            return HttpResponseBadRequest('注册失败')

        # return render(request, 'templates/testcase.html')
        return HttpResponseRedirect('/testcase1/')




# 用例导出
def case_export(request):
    wb = xlwt.Workbook(encoding='utf-8')  # 创建新的Excel
    module_all = DB_module.objects.all()
    # 遍历得到所有的模块
    for module in module_all:
        logger.info("===========目前正在导出的模块是：%s============" % module)
        case_list_all = DB_testcase.objects.filter(t_module=module).values_list()
        ws = wb.add_sheet(module.t_module_name, cell_overwrite_ok=True)
        logger.info("===========Excel增加模块：%s============" % module)
        if len(case_list_all) >= 1:
            i = 0
            # 1, 登录, p1, 验证登录是否成功, 1.。。2。。。3.。。, 环境准备就绪, 登录成功, 登录成功, 登录成功
            for case_list in case_list_all:
                ws.write(i, 0, label=case_list[0])  # 用例编号
                ws.write(i, 1, label=module.t_module_name)  # 所属模块
                ws.write(i, 2, label=case_list[1])  # 优先级
                ws.write(i, 3, label=case_list[2])  # 测试目的
                ws.write(i, 4, label=case_list[3])  # 前置条件
                ws.write(i, 5, label=case_list[4])  # 测试步骤
                ws.write(i, 6, label=case_list[5])  # 预期结果
                ws.write(i, 7, label=case_list[6])  # 备注
                ws.write(i, 8, label=case_list[7])  # 实际结果
                i += 1
            logger.info("===========导出模块：%s 成功============" % module)
    wb.save("%s" % (filename))

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
    logger.info("导出成功")
    return response


# 模块删除
@csrf_exempt
def module_del(request):
    del_module_name = request.POST['del_module_name']
    module = DB_module.objects.get(t_module_name=del_module_name)
    logger.info('====删除模块的名称为：%s===' % module)
    if module != '':
        try:
            case = DB_testcase.objects.filter(t_module=module.id)
            if case:
                case.delete()
                logger.info('====删除模块的id为：%s，删除用例成功===' % module.id)
            # 最后删除掉模块名称
            DB_module.objects.get(t_module_name=module).delete()
            logger.info('====删除模块的名称为：%s，删除模块成功' % module)
            return HttpResponseRedirect('/testcase1/')
        except Exception as e:
            logger.info('====删除%s模块的用例失败===' % module.id)

    return HttpResponseRedirect('/testcase1/')


# 模块添加
@csrf_exempt
def model_one_add(request):
    t_module_name = request.POST['t_module_name']
    if t_module_name != '':

        try:
            DB_module.objects.create(t_module_name=t_module_name)
            logger.info('====添加模块的名称：%s===' % t_module_name)

        except Exception as e:

            logger.info('====添加名称出错：%s===' % t_module_name)
    else:
        logger.info('====非法的输入：%s===' % t_module_name)
        return HttpResponse('非法的输入')
    return HttpResponse('/testcase1/')


# 用例上传
def upload_file(request):
    file = request.FILES['file']
    url = settings.BASE_DIR + '/static/' + file.name
    # 文件复制一份放在static目录下面
    with open(url, 'wb')as f:
        for data in file.chunks():
            f.write(data)

    import xlrd
    # 打开指定路径的Excel文件
    workbook = xlrd.open_workbook(url)
    # 获取所有的sheet
    sheets = workbook.sheets()
    for sheet in sheets:
        # 获取行数
        nrows = sheet.nrows
        # 这种是没有表头的情况，有表头的话需要：for x in range(1, nrows):
        for x in range(0, nrows):
            # row表示某一行的所有数据，是一个列表
            row = sheet.row_values(x)
            DB_testcase.objects.create(
                t_module=DB_module.objects.filter(t_module_name=row[1]).first(),
                t_priority=row[2],  #
                t_purpose=row[3],
                t_precondition=row[4],
                t_steps=row[5],
                t_expected_result=row[6],
                t_actual_result=row[7],
                t_remark=row[8],
            )

    return redirect('/testcase1')


# 用例上传
# def upload_file2(request):
#     # 首先判断文件请求类型
#     if str(request.method).upper() == 'GET':
#         logger.info('GET方法请求：upload_file')
#         return render(request, 'templates/testcase.html')
#
#     elif str(request.method).upper() == 'POST':
#         try:
#             file_obj = request.FILES.get('file')
#             logger.info('上传文件file:%s' % file_obj.name)
#         except Exception as e:
#             logger.info('上传文件为空')
#             # return HttpResponseBadRequest('未上传任何文件')
#             return redirect('/testcase1')
#         file_name_old = file_obj.name
#         # 拼接一下文件名称，避免重复
#         file_name_new = file_name_old.split('.')[0] + time.strftime('%Y%m%d-%H%M%S') + "." + file_name_old.split('.')[1]
#         try:
#             with open('static/' + file_name_new, 'wb') as f:
#                 for line in file_obj.chunks():
#                     f.write(line)
#             f.close()
#             logger.info('读取文件结束')
#         except Exception as e:
#             logger.error('读取文件异常')
#         file_full_path = 'static' + os.sep + file_name_new
#         logger.info('文件路径为：%s' % file_full_path)
#         try:
#             with open(file_full_path, 'r') as f:
#                 reader = csv.reader(f)
#                 for row in reader:
#                     DB_testcase.objects.create(
#                         t_module=DB_module.objects.filter(t_module_name=row[1]).first(),
#                         t_priority=row[2],  #
#                         t_purpose=row[3],
#                         t_precondition=row[4],
#                         t_steps=row[5],
#                         t_expected_result=row[6],
#                         t_actual_result=row[7],
#                         t_remark=row[8],
#                     )
#         except Exception as e:
#             logger.error('上传出现问题%s' % e)
#
#         return redirect('/testcase1')

def testcase3(request):
    logger.info('访问testcase3页面')
    return render(request, 'templates/testcase3.html')


def testcase2(request):
    logger.info('访问testcase2页面')
    # 1.获取所有分类信息
    categories = ArticleCategory.objects.all()
    # 2.接收用户点击的分类id
    cat_id = request.GET.get('cat_id', 1)
    # 3.根据分类id进行分类的查询
    try:
        category = ArticleCategory.objects.get(id=cat_id)
        # print('category',category)
        logger.info('testcase2页面，进入的分类为：', category)
    except ArticleCategory.DoesNotExist:
        logger.info('testcase2页面，没有此分类', )
        return HttpResponseNotFound('没有此分类')
    # 4.获取分页参数
    page_num = request.GET.get('page_num', 1)
    page_size = request.GET.get('page_size', 10)
    # 5.根据分类信息查询文章数据
    articles = Article.objects.filter(category=category)
    logger.info('testcase2页面，查询到的文章为：', articles)
    # 6.创建分页器
    from django.core.paginator import Paginator, EmptyPage
    # paginator=Paginator(articles,per_page=page_size)
    paginator = Paginator(articles, per_page=1)
    # 7.进行分页处理
    try:
        page_articles = paginator.page(page_num)
    except EmptyPage:
        return HttpResponseNotFound('empty page')
    # 总页数
    total_page = paginator.num_pages

    # 8.组织数据传递给模板
    context = {
        'categories': categories,
        'category': category,
        'articles': page_articles,
        'page_size': page_size,
        'total_page': total_page,
        'page_num': page_num
    }
    return render(request, 'templates/testcase2.html', context=context)


def testcase1(request):
    module_id = request.GET.get('module_id', 1)
    # print(module_id)
    logger.info('从前端拿到模块的module_id为：%s' % module_id)
    # 分页的时候会用到，获取页码
    page = request.GET.get('page', 1)
    # 判断页码
    if not page:
        page = 1
    else:
        page = int(page)
    # 取出所有的模块
    all_module = DB_module.objects.all()
    # print(all_module)
    logger.info('取出所有的模块为：%s' % all_module)
    try:
        module_case = DB_module.objects.get(id=module_id)

    except Exception as e:
        print(e)
        return HttpResponseBadRequest('无用例')
        # module_case = DB_module.objects.get(id=1)
    # 获取所有的测试用例
    # all_testcase = DB_testcase.objects.all()
    # 获取该模块下所有的测试用例
    all_testcase_module = DB_testcase.objects.filter(t_module=module_case)
    paginator = Paginator(all_testcase_module, 15)
    page_article_list = paginator.page(page)
    pag_num = paginator.num_pages
    # 判断是否存在下一页
    if page_article_list.has_next():
        next_page = page + 1
    else:
        next_page = page
    if page_article_list.has_previous():
        prev_page = page - 1
    else:
        prev_page = page
    # 获取总页码数
    print(module_id)
    page_num = range(1, pag_num + 1)
    print(page_num)
    # return render(request, 'templates/testcase.html', context={"testcase": v_testcase})
    return render(request, 'templates/testcase6.html', {
        'page_article_list': page_article_list,
        'page_num': page_num,
        'testcase_list': page_article_list,
        'curr_page': page,
        'next_page': next_page,
        'prev_page': prev_page,
        'module_list': all_module,
        'module_id': module_id
    })
