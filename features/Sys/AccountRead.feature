Feature: 系统信息相关

  Background: 设置http头
  * http请求http头设置
  |key |value|
  |Connection| keep-alive|

#--------------------------------------------------------------------------------------------------------------------------------------
  Scenario: [1-1]获取用户的广告账号列表
    * http请求参数设置
      | key      | value                    |
      | status | ACTIVE |
    * [Http]发送httpGet请求--API接口/index.php/sys/accounts/read
    * 服务器返回成功，检查返回码200
    * 检查接口返回结果中包含以下所有内容
      | key      |
      |{"code":0,"msg":"success"|
    * 数据库校验用户广告账号信息

