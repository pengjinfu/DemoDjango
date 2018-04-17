import os
import django
'''
在service测试需要加载settings.py，这样才能够调用app->services/models的方法
1. 加载DJANGO_SETTINGS_MODULE的基本配置信息
2. 加载django的基础执行模块，从而来使用django库和方法

不加载以下2段代码会报如下的错误：
1. Settings 'Improperly Configured' Error
2. AppRegistryNotReady: Apps aren't loaded yet
'''

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "demo_django.settings")
django.setup()