from django.core.paginator import Paginator
from django.shortcuts import render

# Create your views here.
from CaseManagement.models import DB_testcase


def testcase(request):
    page = request.GET.get('page')
    if not page:
        page = 1
    else:
        page = int(page)

    all_testcase = DB_testcase.objects.all()
    paginator = Paginator(all_testcase, 5)

    page_article_list = paginator.page(page)
    pag_num = paginator.num_pages
    if page_article_list.has_next():
        next_page = page + 1
    else:
        next_page = page
    if page_article_list.has_previous():
        prev_page = page - 1
    else:
        prev_page = page
    page_num = range(1, pag_num+1)
    print(page_num)
    # return render(request, 'templates/testcase.html', context={"testcase": v_testcase})
    return render(request, 'testcase.html', {
        'page': page_article_list,
        'page_num': page_num,
        'testcase_list':page_article_list,
        'curr_page': page,
        'next_page': next_page,
        'prev_page': prev_page,
    })
