#/*********************************************
#*  使用django 框架
#*  使用request 来请求接口获取数据
#*********************************************/
import sys

## 引入类的操作，
from Mingrenmingyan import  Mingrenmingyan
famous_word = Mingrenmingyan();
data = famous_word.get_mrmy();
print(data);exit();

