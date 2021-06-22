from django.core.paginator import Paginator
from django.http import HttpResponseBadRequest
from django.shortcuts import render

# Create your views here.
from CaseManagement.models import DB_testcase, DB_module


def testcase(request):
    # 从前端拿到模块的id
    module_id = request.GET.get('module_id', 1)
    # 分页的时候会用到，获取页码
    page = request.GET.get('page')
    # 判断页码
    if not page:
        page = 1
    else:
        page = int(page)
    # 取出所有的模块
    all_module = DB_module.objects.all()

    try:
        module_case = DB_module.objects.get(id=module_id)
    except Exception as e:
        print(e)
        return HttpResponseBadRequest('无此分类')
    # 获取所有的测试用例
    # all_testcase = DB_testcase.objects.all()
    all_testcase_module = DB_testcase.objects.filter(t_module=module_case)
    paginator = Paginator(all_testcase_module, 5)
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

    page_num = range(1, pag_num + 1)
    print(page_num)
    # return render(request, 'templates/testcase.html', context={"testcase": v_testcase})
    return render(request, 'templates/testcase.html', {
        'page': page_article_list,
        'page_num': page_num,
        'testcase_list': page_article_list,
        'curr_page': page,
        'next_page': next_page,
        'prev_page': prev_page,
        'module_list': all_module,
        'module_case': module_case
    })
