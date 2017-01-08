from django.shortcuts import render
from django.http import HttpResponse
import json
from article.models import Article


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
def detail(request, my_args):
    #post = Article.objects.all()[int(my_args)]
    #pars =  request.params;
    test = Article.test('aaaabb');
    # str = ("title = %s, category = %s, date_time = %s, content = %s"
    #     % (post.title, post.category, post.date_time, post.content))
    # return HttpResponse(str)
    #str =  json.dump(pars);
    return HttpResponse("Use article test method result 2 : " + my_args + test );