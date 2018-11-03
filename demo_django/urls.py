"""demo_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from article import  views


urlpatterns = [

    url(r'^admin/', admin.site.urls),
    # 查看view的home方法操作
    url(r'^$', views.home),  # 由于目前只有一个app, 方便起见, 就不设置include了
    # 对ajax的数据的处理
    url(r'^ajax_dict/$', views.ajax_dict, name='ajax_dict'),

    # 复杂的url的处理
    url(r'^(?P<my_args>\d+)/$', views.detail, name='detail'),

    # 增加模板url
    url(r'^test/$', views.test, name='test'),

    # Redis 操作
    url(r'^redis/$', views.redis, name='redis'),
]

# urlpatterns = patterns('',
#     # Examples:
#     # url(r'^$', 'my_blog.views.home', name='home'),
#     # url(r'^blog/', include('blog.urls')),
#
#     url(r'^admin/', include(admin.site.urls)),
#     url(r'^$', 'article.views.home'),  #由于目前只有一个app, 方便起见, 就不设置include了
# )
