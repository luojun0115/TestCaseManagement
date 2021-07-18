# -*- coding: utf-8 -*-
import csv
import datetime
import json
import os
import time

from django.core.paginator import Paginator
from django.http import HttpResponseBadRequest, HttpResponseNotFound, HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from CaseManagement.models import DB_testcase, DB_module, Article, ArticleCategory
from TestCaseManagement.settings import logger


# 用例导出
def case_export(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=%s.csv' % (
        datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    )
    response.charset = 'utf-8'
    import xlwt  # 导入模块
    wb = xlwt.Workbook(encoding='ascii')  # 创建新的Excel
    module_all = DB_module.objects.all()
    # 遍历得到所有的模块
    for module in module_all:
        logger.info("===========目前正在导出的模块是：%s============" % module)
        case_list_all = DB_testcase.objects.filter(t_module=module).values_list()

        ws = wb.add_sheet(str(module.t_module_name), cell_overwrite_ok=True)
        logger.info("===========Excel增加模块：%s============" % module)
        if len(case_list_all) >= 1:
            i = 0
            # 1, 登录, p1, 验证登录是否成功, 1.。。2。。。3.。。, 环境准备就绪, 登录成功, 登录成功, 登录成功
            for case_list in case_list_all:
                print(case_list)
                ws.write(i, 0, label=str(case_list[0]))  # 用例编号
                ws.write(i, 1, label=str(module.t_module_name))  # 所属模块
                ws.write(i, 2, label=str(case_list[1]))  # 优先级
                ws.write(i, 3, label=str(case_list[2]))  # 测试目的
                ws.write(i, 4, label=str(case_list[3]))  # 前置条件
                ws.write(i, 5, label=str(case_list[4]))  # 测试步骤
                ws.write(i, 6, label=str(case_list[5]))  # 预期结果
                ws.write(i, 7, label=str(case_list[6]))  # 备注
                ws.write(i, 8, label=str(case_list[7]))  # 实际结果
                i += 1
            logger.info("===========导出模块：%s 成功============" % module)
    wb.save(response)
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
    # 首先判断文件请求类型
    if str(request.method).upper() == 'GET':
        logger.info('GET方法请求：upload_file')
        return render(request, 'templates/testcase.html')

    elif str(request.method).upper() == 'POST':
        try:
            file_obj = request.FILES.get('file')
            logger.info('上传文件file:%s' % file_obj.name)
        except Exception as e:
            logger.info('上传文件为空')
            # return HttpResponseBadRequest('未上传任何文件')
            return redirect('/testcase1')
        file_name_old = file_obj.name
        # 拼接一下文件名称，避免重复
        file_name_new = file_name_old.split('.')[0] + time.strftime('%Y%m%d-%H%M%S') + "." + file_name_old.split('.')[1]
        try:
            with open('static/' + file_name_new, 'wb') as f:
                for line in file_obj.chunks():
                    f.write(line)
            f.close()
            logger.info('读取文件结束')
        except Exception as e:
            logger.error('读取文件异常')
        file_full_path = 'static' + os.sep + file_name_new
        logger.info('文件路径为：%s' % file_full_path)
        try:
            with open(file_full_path, 'r',encoding='utf-8') as f:
                reader = csv.reader(f)
                for row in reader:
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
        except Exception as e:
            logger.error('上传出现问题%s' %e)

        return redirect('/testcase1')


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
