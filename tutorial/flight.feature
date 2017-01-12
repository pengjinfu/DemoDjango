Feature:  广告管理信息相关
  In order to increase the ninja survival rate,
  As a ninja commander
  I want my ninjas to decide whether to take on an
  opponent based on their skill levels   中国
 Background: 设置http头
  * http请求http头设置
  |key |value|
  |Connection| keep-alive|
  * http请求设置局部Cookie

Scenario: [1-1]获取Ad的FB信息
   * http请求参数重置
     | name      | department  |
     | Barry     | Beer Cans   |
     | Pudey     | Silly Walks |
     | Two-Lumps | Silly Walks |

* http请求特殊参数设置message
    '''
    {"objective":"MOBILE_APP_INSTALLS","application_id":"116913278412853","platform":"Android","app_url":"http://play.google.com/store/apps/details?id=com.wantu.activity","page_id":"490509417821868","name":"_||OS_Date"}
    '''
    * [Http]发送httpPost请求--API接口/index.php/ad/adtemplate/create
    * 服务器返回成功，检查返回码200
    * 检查接口返回结果中包含以下所有内容
        | key      |
      |{"code":0,"msg":"success"|