from django.core.paginator import Paginator
from django.http import HttpResponseBadRequest, HttpResponseNotFound
from django.shortcuts import render

# Create your views here.
from CaseManagement.models import DB_testcase, DB_module,Article,ArticleCategory


def testcase(request):
    # 1.获取所有分类信息
    categories = ArticleCategory.objects.all()
    # 2.接收用户点击的分类id
    cat_id = request.GET.get('cat_id', 1)
    # 3.根据分类id进行分类的查询
    try:
        category = ArticleCategory.objects.get(id=cat_id)
        print('category',category)
    except ArticleCategory.DoesNotExist:
        return HttpResponseNotFound('没有此分类')
    # 4.获取分页参数
    page_num = request.GET.get('page_num', 1)
    page_size = request.GET.get('page_size', 10)
    # 5.根据分类信息查询文章数据
    articles = Article.objects.filter(category=category)
    print('articles',articles)
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
    return render(request, 'templates/testcase2.html',context=context)

# def testcase(request):
#     # 从前端拿到模块的id
#     module_id = request.GET.get('module_id',1)
#     print(module_id)
#     # 分页的时候会用到，获取页码
#     page = request.GET.get('page',1)
#     # 判断页码
#     if not page:
#         page = 1
#     else:
#         page = int(page)
#     # 取出所有的模块
#     all_module = DB_module.objects.all()
#     print(all_module)
#
#     try:
#         module_case = DB_module.objects.get(id=module_id)
#
#     except Exception as e:
#         print(e)
#         return HttpResponseBadRequest('无用例')
#         # module_case = DB_module.objects.get(id=1)
#     # 获取所有的测试用例
#     # all_testcase = DB_testcase.objects.all()
#     # 获取该模块下所有的测试用例
#     all_testcase_module = DB_testcase.objects.filter(t_module=module_case)
#     paginator = Paginator(all_testcase_module, 1)
#     page_article_list = paginator.page(page)
#     pag_num = paginator.num_pages
#     # 判断是否存在下一页
#     if page_article_list.has_next():
#         next_page = page + 1
#     else:
#         next_page = page
#     if page_article_list.has_previous():
#         prev_page = page - 1
#     else:
#         prev_page = page
#     # 获取总页码数
#     print(module_id)
#     page_num = range(1, pag_num + 1)
#     print(page_num)
#     # return render(request, 'templates/testcase.html', context={"testcase": v_testcase})
#     return render(request, 'templates/testcase.html', {
#         'page_article_list': page_article_list,
#         'page_num': page_num,
#         'testcase_list': page_article_list,
#         'curr_page': page,
#         'next_page': next_page,
#         'prev_page': prev_page,
#         'module_list': all_module,
#         'module_id': module_id
#     })
