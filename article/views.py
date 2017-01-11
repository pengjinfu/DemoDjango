from django.shortcuts import render
from django.http import HttpResponse
import json
from article.models import Article
from datetime import datetime
from django.conf import settings
from django.core.cache import cache
from article.services import ArticleServices

# Create your views here.
def home(request):
    return HttpResponse("Hello World, Django")

# 简答的Ajax的请求操作
def ajax_dict(request):

    name_dict = {
        'twz': 'Love python and Django',
        'zqxt': 'I am teaching Django',
    }
    return HttpResponse(json.dumps(name_dict), content_type='application/json')

# 在view层就直接使用model的方法
def detail(request,my_args):
    services =  ArticleServices();
    test = services.detail()
    return HttpResponse("Use article test method result : " + test );

# 对使用模板进行测试操作
def test(request) :
    return render(request, 'test.html', {'current_time': datetime.now()})

# 对redis 的基本操作
def redis(request) :
    user_name = 'test'
    key = 'user_id_of_' + user_name
    cache.set(key, json.dumps(user_name), settings.NEVER_REDIS_TIMEOUT)
    value = cache.get(key)
    return HttpResponse('Redis operation ~' + value)