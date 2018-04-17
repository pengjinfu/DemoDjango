Demo_django

####一、 项目描述：
Demo_django是对python django 框架的实践。 django 是非常轻便的框架。 查看： https://www.djangoproject.com/

####二、 它的特点：
1. 轻巧，便捷。 支持很多快速开发的工具和优雅的设计
2. 它侧重与把每个模块作为app,这样方便模板直接的解耦，同时也可以快速的开发。（Django注重组件的重用性和“可插拔性”，敏捷开发和DRY法则（Don't Repeat Yourself））
3. 优秀的辅助功能： app 生成，model与表的生成，命令支持model直接数据的填充和model数据的操作
4. 免费，开源。有强大的社区支持

####三、 它的History, 查看：https://zh.wikipedia.org/wiki/Django
1. 2005年7月成立， 并 Django于2008年6月17日正式成立基金会。
1. Django 的历史比较长，来源于一个每天服务于数百万次页面查看请求的在线报纸服务。
2. Django 项目来源于迅速变化的在线出版业，它重点关注的是一个可以快速构建并修改基于内容的应用程序的框架

####四、 内置应用
1. 一个可扩展的认证系统
2. 动态站点管理页面
3. 一组产生RSS和Atom的工具
4. 一个灵活的评论系统
5. 产生Google站点地图（Google Sitemaps）的工具
6. 防止跨站请求伪造（cross-site request forgery）的工具
7. 一套支持轻量级标记语言（Textile和Markdown）的模板库
8. 一套协助创建地理信息系统（GIS）的基础框架

####五、 项目的目标
#####1.  部署和执行django的项目
###### 1) 基本的MVC的操作 
- 【done】启动django的应用服务（切换到项目的目录）：python manage.py runserver [查看](https://andrew-liu.gitbooks.io/django-blog/content/xiang_mu_yu_app.html)
- 【done】django 的ajax的处理
- 【done】在开发环境关闭缓存，在settings.py进行设置 ，[查看](http://www.dongcoder.com/detail-211402.html)
- 【done】对框架的模板操作，[查看](https://docs.djangoproject.com/en/1.10/topics/templates/)
- 【done】页面的http的请求： Controller->model->Controller->View [Django 采用 urls配置的方式]
- 【done】完成基本的数据的接口的交互[支持url的接口请求并相应的处理]
- 【done】Python 的多线程的处理，使用自带的线程库处理 [查看](http://www.runoob.com/python/python-multithreading.html)

###### 2） 包括命令行的使用（对内）
- 【done】生成app/模块的命令：django-admin.py startproject YOUR_APP_NAME [查看](https://andrew-liu.gitbooks.io/django-blog/content/xiang_mu_yu_app.html)
- 【done】进行model操作的命令： python manage.py shell  [查看](https://andrew-liu.gitbooks.io/django-blog/content/models.html)

###### 3） 组件的使用，如mysql,sqlite, redis, mongo 等
- 【done】支持多个库的操作和使用 ，[查看](https://segmentfault.com/a/1190000003555520)
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
    'auth_db': {
        'NAME': 'auth_db',
        'ENGINE': 'django.db.backends.mysql',
        'USER': 'mysql_user',
        'PASSWORD': 'swordfish',
    },
    'primary': {
        'NAME': 'primary',
        'ENGINE': 'django.db.backends.mysql',
        'USER': 'mysql_user',
        'PASSWORD': 'spam',
    },
    'replica1': {
        'NAME': 'replica1',
        'ENGINE': 'django.db.backends.mysql',
        'USER': 'mysql_user',
        'PASSWORD': 'eggs',
    },
    'replica2': {
        'NAME': 'replica2',
        'ENGINE': 'django.db.backends.mysql',
        'USER': 'mysql_user',
        'PASSWORD': 'bacon',
    },
}
```
- 【done】使用sqlite的操作：同上
- 【done】使用mysql的操作：需要安装mysql的扩展：pip install PyMySQL  配置同上 (这MySQL-python 扩展在python 3.5之后再mysql官方找不到驱动)，[查看](https://github.com/PyMySQL/PyMySQL/)
- 【done】使用redis的操作：pip install redis [查看](https://github.com/sebleier/django-redis-cache)
```
CACHES = {
    'default': {
        'BACKEND': 'redis_cache.cache.RedisCache',
        'LOCATION': '127.0.0.1:6379',
        "OPTIONS": {
            "CLIENT_CLASS": "redis_cache.client.DefaultClient",
        },
    },
}
REDIS_TIMEOUT=7*24*60*60
CUBES_REDIS_TIMEOUT=60*60
NEVER_REDIS_TIMEOUT=365*24*60*60
```
- 使用mongo的操作：pip install mongoengine==0.8.0  [查看](http://staltz.com/djangoconfi-mongoengine/#/8)

#####2. 能够了解django中自动加载库和管理第三方库
- 【done】python的第三方库的自动加载 ,[单个加载](http://www.jianshu.com/p/41a9c25273b1),[批量加载](http://lazybios.com/2015/06/how-to-use-requirementstxt-file-in-python/)
```
生成requirements.txt文件
pip freeze > requirements.txt
安装requirements.txt依赖
pip install -r requirements.txt
```
- 一些常用的第三方库/组件库 ， [查看](http://dudu.zhihu.com/story/8083778)
- 自建构建第三方库进行加载[这个暂时不需要]


#####3. 集成SDK的处理，包括http的各种操作


#####4. 支持对django的单元测试/集成测试的工作
- 【done】常用的单元测试框架：[unittest](https://docs.python.org/3/library/unittest.html),[pyunit](http://pyunit.sourceforge.net/pyunit_cn.html) , [behave](http://pythonhosted.org/behave/)
- 【done】unittest框架使用demo 见 tests 目录 ， 运行：python -m unittest tests/test_something.py  或者 python -m unittest -v tests/test_something.py
- 【done】behave框架使用： pip install -U behave  , 支持behave 来自动化测试开发的项目，详见目录 tutorial 和 features ， 命令：behave features   --junit --junit-directory='/reports' -D ENV=TEST  --tags=-no 
- 【暂时没研究】PyUnit的框架
- 【done】使用测试框架编写测试的demo,支持对django的service/model的测试， 命令：python -m unittest tests\services\ArticleServiceTest.py

- 集成框架的支持：

#####5. 对django 的自动处理
- 研究django的框架的源代码：python\Lib\site-packages\django
- 【done】对django的框架的优化，使其支持service层级
- 【done】熟悉django的模板机制
- 工具的集成处理

####六、 其他

####七、 常见问题
###### 1. behave given 不支持中文，会报"UnicodeDecodeError: 'gbk' codec can't decode byte 0x80 in position 265: illegal multibyte sequence"
> 解决方法：对behave\runner.py源码进行修改，[查看](https://github.com/behave/behave/issues/361)
```
## 改前：
def exec_file(filename, globals={}, locals=None):
    if locals is None:
        locals = globals
    locals['__file__'] = filename
    with open(filename) as f:
## 改后：
def exec_file(filename, globals={}, locals=None):
    if locals is None:
        locals = globals
    locals['__file__'] = filename
    with open(filename, "rb") as f:

```
