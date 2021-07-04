from django.conf.urls import url
from django.urls import include

from . import views

# urlpatterns是被django自动识别的路由列表变量
urlpatterns = [
    # 每个路由信息都需要使用url函数来构造
    # url(路径, 视图)
    url(r'testcase1/', views.testcase1),
    url(r'testcase2/', views.testcase2),
    url(r'testcase3/', views.testcase3),
    url(r'upload_file/', views.upload_file),  # 上传测试用例
]
