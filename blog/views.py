from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render

# Create your views here.
from blog.models import Article, ArticleCategory


def article_content(request):
    page = request.GET.get('page')
    cat_id = request.GET.get('cat_id', 1)
    print(cat_id)
    categories = ArticleCategory.objects.all()


    try:
        category = ArticleCategory.objects.get(id=cat_id)
    except Exception as e:
        print(e)
        return HttpResponseBadRequest('无此分类')

    if page:
        page = int(page)
    else:
        page = 1
    # if int(cat_id) !=1:
    all_article = Article.objects.filter(category=category)
    # else:
    #     all_article = Article.objects.all()
    paginator = Paginator(all_article, 1)

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
    print('categories',categories)
    top_article_list = Article.objects.order_by('-publish_date')[:5]
    return render(request, 'article.html', {'article_list': page_article_list,
                                            'page_num': range(1, pag_num + 1),
                                            'curr_page': page, 'next_page': next_page,
                                            'prev_page': prev_page,
                                            'top_article_list': top_article_list,
                                            'category': category,
                                            'categories':categories

                                            })


def get_detail_content(request, article_id):
    all_article = Article.objects.all()
    print(all_article)

    curr_article = None
    Previous_index = 0
    Next_index = 0
    for index, article in enumerate(all_article):
        if index == 0:
            Previous_index = 0
            Next_index = index + 1
        elif index == len(all_article) - 1:
            Previous_index = index - 1
            Next_index = index
        else:
            Previous_index = index - 1
            Next_index = index + 1
        if article.article_id == int(article_id):
            print('article.article_id', article.article_id)
            curr_article = article
            Previous_article = all_article[Previous_index]
            Next_article = all_article[Next_index]
            print('curr_article:', curr_article)
            break
    # print(curr_article)
    return render(request, 'detail.html', {'curr_article': curr_article,
                                           "Previous": Previous_article, 'Next': Next_article,


                                           })
    # return render(request, 'detail.html', {'curr_article': curr_article})
