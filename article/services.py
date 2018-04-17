import json
from article.models import Article
from datetime import datetime
from django.conf import settings
from django.core.cache import cache
"""
    services 层的介绍
    1. services 是基于控制器和model之前的一层，它的作用在于处理大量的业务逻辑以及代码的复用
    2. django 里面的views 就类似 其他的web语言的controller ， 而其他web语言的views层相当于django里面的template
    3. django 的views 主要做的事情， 包括输入参数的验证，如http请求的参数，对业务处理返回的结果json数据，使用HttpReponse 返回输出
    4. 由于主要的业务是放在services层级，后期所有的单元测试/集成测试也是针对services的文件进行验证和操作
    5. 关联关系： views可以调用多个services, 一个services 可以使用多个models或者db组件，
"""
class ArticleServices() :

    # 在view层就直接使用model的方法
    def detail(self):

        test = Article.test('aaaabb')
        return test;
