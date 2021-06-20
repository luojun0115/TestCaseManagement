from django.conf.urls import url

from blog import views

urlpatterns = [
    # 每个路由信息都需要使用url函数来构造
    # url(路径, 视图)
    url(r'article_content/$', views.article_content),
    # url(r'get_detail_content/$',views.get_detail_content),
    # url('get_detail_content/(\d{1})/',views.get_detail_content),
    url('get_detail_content/(?P<article_id>\d+)/', views.get_detail_content),
    # url(r'^weather/(?P<city>[a-z]+)/(?P<year>\d{4})/$', views.weather),

]
