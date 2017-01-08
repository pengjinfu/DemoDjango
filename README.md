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
- django 的ajax的处理
- 页面的http的请求： Controller->model->Controller->View
- 完成基本的数据的接口的交互

###### 2） 包括命令行的使用（对内）
- 生成app/模块的命令
- 进行model操作的命令

###### 3） 组件的使用，如mysql,sqlite, redis, mongo 等
- 使用sqlite的操作：
- 使用mysql的操作：
- 使用redis的操作：
- 使用mongo的操作：

#####2. 能够了解django中自动加载库和管理第三方库
- python的第三方库的自动加载
- 自建构建第三方库进行加载

#####3. 集成SDK的处理，包括http的各种操作
#####4. 支持对django的单元测试/集成测试的工作
- 常用的单元测试框架：
- 使用测试框架编写测试的demo,支持对django的service/model的测试
- 集成框架的支持：

#####5. 对django 的自动处理
- 研究django的框架的源代码：python\Lib\site-packages\django
- 对django的框架的优化，使其支持service层级
- 熟悉django的模板机制
- 工具的集成处理

####六、 其他
