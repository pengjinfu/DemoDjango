# -*- coding: utf-8 -*-
'''
@author: redstar
'''

from behave import given, when, then, step
from features.utils.http_req import Request
from features.utils.func import *
from features.steps import ANDROIDHTTPHEADER
from features.utils.base64_coder import Base64Coder
from hamcrest import *  # @UnusedWildImport
import time
import json
import random
import copy
from features.steps.mongo_op import *
from features.steps.mysql_op import *
from  urllib.parse import quote,urlencode


#########################----------http请求-------######################################
@given(u'[{httpHost:S}]发送{mode:S}请求--API接口{api:S}')
def send_request(context, httpHost, mode, api,retryNum =0):
    Header = {}
    httpMode = "GET"
    PostData = {}
    paramData = {}

    context.feature.Retry = 0

    #设置http请求host，从steps/config.py文件中获取host
    if httpHost in context.feature.httpHosts:
        httpHost = context.feature.httpHosts[httpHost]

    #使用post还是get方式发送http请求
    if mode == "httpPost":
        httpMode = "POST"
    api = requestUrl(context,api)

    #拼接请求URI
    URL = "http://%s" % httpHost + api.strip()
    # print(context.text)

    #获取请求参数
    if hasattr(context, "params"):
        paramData = getattr(context, "params")
    # print("http请求参数："+paramData)

    #如果是get请求，直接在URI后边加上 ?param1=val1&param2=val2
    #如果是post请求，则需要post body
    # if httpMode == "GET":
    #     params = ""
    #     for item in paramData.keys():
    #         params = params + str(item)+"="+str(paramData[item])+"&"
    #     URL = URL + "?" + params[:-1]
    # else:
    #         PostData = paramData

    # 添加http头，修改http头 以及删除http头
    # 1.先判断context.feature.Header，存在的话先用context.feature
    # 2.再判断context.Header,存在的话，替换context.feature.Header
    if hasattr(context.feature, "Header"):
        Header = getattr(context.feature, "Header")
    if hasattr(context, "Header"):
        Header = getattr(context, "Header")

    if hasattr(context.feature, "token"):
            Header["Cookie"] = getattr(context.feature, "token")
    elif hasattr(context, "token"):
            Header["Cookie"] = getattr(context, "token")

    if hasattr(context, "addHeader"):
        addHeader1 = getattr(context, "addHeader")
        for key1 in addHeader1:
            Header[key1] = addHeader1[key1]
    if hasattr(context.feature, "addHeader"):
        addHeader2 = getattr(context.feature, "addHeader")
        for key2 in addHeader2:
            Header[key2] = addHeader2[key2]
    if hasattr(context, "delHeader"):
        delHeader = getattr(context, "delHeader")
        for key in delHeader:
            if key in Header:
                del Header[key]
    print("请求方式: " + httpMode)
    print("请求地址: " + URL)
    print("请求Http头:")
    HeaderTtmp = copy.copy(Header)
    for headInfo in HeaderTtmp:
        print(headInfo + ":" + HeaderTtmp[headInfo])
    if httpMode == "POST":
        #print("Post数据: " + str(PostData))
        context.response = Request(URL, headers=Header, data=paramData, method=httpMode).send_request()
    else:
        params = ""
        for item in paramData.keys():
            params = params + str(item)+"="+str(paramData[item])+"&"
        URL = URL + "?" + params[:-1]
        context.response = Request(URL, headers=Header).send_request()

    if retryNum>0 :
        print("Have retry HttpRequest for "+str(retryNum)+" time....")
    try:
        ResponseBody = json.loads(context.response.get("body"), encoding='utf-8')
        ResponseHeader = context.response.get("headers")
    except:
        #重试机制
        time.sleep(1)
        if retryNum < 3:
            retryNum = retryNum +1
            send_request(context, httpHost, mode, api,retryNum)
    else:

        context.feature.data = ResponseBody
        context.feature.headers = ResponseHeader
        # time.sleep(1)

#处理请求URL中的参数 :  $param$ 变成 $param，然后根据 $param将变量转化为value
def requestUrl(context,url):
    flag = False
    strTmp = ""
    KeyVal = {}
    for i in range(len(url)):
        if url[i] == "$":
            #开始了
            if flag is False:
                flag = True
            else:
                KeyVal["$"+strTmp+"$"] = paramArgs(context,"$"+strTmp)
                flag = False
            strTmp = ""
        elif flag is True:
            strTmp = strTmp + url[i]
    for info in  KeyVal:
            url = url.replace(info,KeyVal[info])
    return url

# 设置整个feature范围内的http头
@given(u'[Feature]http请求http头设置')
def setFHttpRequestHeaders(context):
    if hasattr(context.feature, "Header"):
        context.feature.Header = getattr(context.feature, "Header")
    else:
        context.feature.Header = {}
    for info in context.table:
        context.feature.Header[info["key"]] = info["value"]

@given(u'http请求设置局部Cookie')
def resetHttpCookie(context):
    if hasattr(context, "mgrtoken"):
        context.feature.token = getattr(context, "mgrtoken")

# 设置Scenario范围内的http头
@given(u'http请求http头设置')
def setHttpRequestHeaders(context):
    if hasattr(context, "Header"):
        context.Header = getattr(context, "Header")
    else:
        context.Header = {}
    for info in context.table:
        context.Header[info["key"]] = info["value"]

@given(u'设置登录信息')
def addLoginInfos(context):
    context.addHeader = {}
    if hasattr(context, "username"):
        username = getattr(context, "username")
    if hasattr(context, "password"):
        password = getattr(context, "password")
    baseCode = 'Basic '+Base64Coder(username+':'+password).encode()
    context.addHeader['authorization'] = baseCode

@given(u'保存登录成功认证')
def saveLoginInfos(context):
    context.feature.addHeader = {}
    cookies = context.response.get("headers")
    cookie = cookies.get("Set-Cookie")
    context.feature.addHeader['Cookie'] = cookie

# 如果存在Feature范围的http头，则先将Feature范围的http头设置为Scenario范围内的http头，然后再进行删除
@given(u'删除http请求http头设置')
def delHttpRequestHeaders(context):
    context.delHeader = {}
    for info in context.table:
        context.delHeader[info["key"]] = info["key"]

# 如果存在Feature范围的http头，则先将Feature范围的http头设置为Scenario范围内的http头，然后进行修改
@given(u'添加修改http请求http头设置')
def addHttpRequestHeaders(context):
    context.addHeader = {}
    for info in context.table:
        context.addHeader[info["key"]] = info["value"]

# @given(u'http请求参数设置')
# def setHttpRequestParams(context):
#     paramTmp = ""
#     for info in context.table:
#          if info.get("key"):
#              valuea = getParamValue(context,info["value"].strip())
#              paramTmp = paramTmp + info["key"] + "=" + valuea + "&"
#     if hasattr(context, "params"):
#         params = getattr(context, "params")
#         params = params + "&" + paramTmp
#     else:
#         params = paramTmp
#     context.params = params[:-1]

@given(u'http请求参数设置')
def setHttpRequestParams(context):
    paramTmp = {}
    if hasattr(context, "params"):
        paramTmp = getattr(context, "params")
    for info in context.table:
         if info.get("key"):
             valuea = getParamValue(context,info["value"].strip())
             paramTmp[info["key"]] =  valuea
    context.params = paramTmp


@given(u'http请求特殊参数设置{param:S}')
def setHttpRequestTParams(context, param):
    paramTmp = {}
    if hasattr(context, "params"):
        paramTmp = getattr(context, "params")
    pValue = getParamValue(context,context.text)
    paramTmp[param] =  pValue
    context.params = paramTmp

@given(u'http请求参数重置')
def resetHttpRequestParams(context):
    paramTmp = {}
    for info in context.table:
         if info.get("key"):
             valuea = getParamValue(context,info["value"].strip())
             print(valuea)
             paramTmp[info["key"]] =  valuea
    context.params = paramTmp

###更新对参数类型 AAA$BBB$CCC   最终为 AAA+转义之后的参数 + CCC格式
### author : Wilson
def formatArgs(context, param):
    param = str(param).lower()
    if hasattr(context, param):
        param = getattr(context, param)
    elif hasattr(context.feature, param):
        param = getattr(context.feature, param)
    return  param


def getParamValue(context,param):
    param = str(param)
    if param.find("$") == -1:
        return param
    elif param.find("$") == 0 and param.count("$") == 1:
        param = "*"+param+"$*"
    else:
        param = "*"+param+"*"
    params = param.split("$")
    returnStr = ""
    flag = 0
    for item in params:
        if flag == 0:
            returnStr = returnStr+item
            flag = 1
        elif flag == 1:
            #目前不支持参数中含有=的请求，比如  p1={aaa=bbb},所有删除=
            strTmp = formatArgs(context,item)
            #strTmp = strTmp.replace("=","")
            returnStr = returnStr+ strTmp
            flag = 0
    returnStr = returnStr[:-1]
    returnStr = returnStr[1:]
    return  returnStr

@given(u'httpPost请求设置body')
def setHttpRequestParams(context):
    context.params = context.text


@given(u'服务器返回成功，检查返回码{code:d}')
def check_response_data(context, code):
    assert_that(context.response.get("http_status"), equal_to(code))


@given(u'检查接口返回结果中可能包含以下内容')
def check_response_data1(context):
    result = False
    for info in context.table:
        tmp = info["key"].strip() in context.response.get("body")
        result = result or tmp
    assert_that(True, equal_to(result))


@given(u'检查接口返回结果中包含以下所有内容')
def check_response_data2(context):
    for info in context.table:
        assert_that(context.response.get("body"), contains_string(getParamValue(context,info["key"].strip())))


@given(u'还原用户订阅列表')
def reverce(context):
    userid = "asdadadsdasd"
    Lang = "asdsadjiwqjdijasd"
    UserFeeds = {}
    if hasattr(context, "userid"):
        userid = getattr(context, "userid")
    if hasattr(context, "userid"):
        userid = getattr(context, "userid")
    if hasattr(context, "userid"):
        userid = getattr(context, "userid")
    sql2 = {"$set": {result: point}}
    mongo_update(env, dbname, collection, sql1, sql2)

@given(u'查询SQL为{sql},检查{strTemp}')
def then_impl(context,sql,strTemp):
    context.sql_result, context.sql_amount = run_sql(sql)
    print("sql_result is :",context.sql_result)
    print("context.sql_amount is :",context.sql_amount)
    assert_that(str(context.sql_result), contains_string(strTemp))

@given(u'判断接口是否已经去重--用户{userid}新闻{newsid}')
def is_Repeat(context,userid,newsid):
    userid = paramArgs(context,userid)
    newsid = paramArgs(context,newsid)
    hostStr = context.feature.httpHosts["httpHost_V2"]
    #这个请求在测试和预发布生产都有的，用于判断用户队列中新闻是否去重，返回true表示用户newsid已读
    URL = "http://"+hostStr+"/v2/repeat?newsId="+newsid+"&userId="+userid+"&client=gatling";
    response = Request(URL).send_request()
    assert_that(response.get("body"), contains_string("true"))


@given(u'判断响应JSON中{attr:S}的值为{value:S}')
def RespValue(context,attr,value):
    myvalue = context.feature.data
    attrDic = {}
    if attr is not "All":
        #先处理Attr
        attrTmp = attr.split("#")
        for tmp in attrTmp:
            if tmp is not None:
                if tmp.isdigit():
                    myvalue = myvalue[int(tmp)]
                else:
                    myvalue = myvalue[str(tmp)]
        assert_that(str(myvalue), equal_to(value))

@given(u'获取http响应包中的{Composekey:S}值，保存为参数{param:S}')
def setAttr(context,Composekey,param):
    myValue = getValue(Composekey,context.feature.data)
    if type(myValue) is dict:
        myValue = json.dumps(myValue)
        myValue = str(myValue)
        myValue = dowithStr(context,myValue)
        #myValue = myValue.replace("=","")
    else:
        myValue = str(myValue)

    setattr(context.feature,param,myValue)
    print(myValue)

@given(u'判断字符串{Str1}是否等同字符串{Str2}')
def strCompare(context,Str1,Str2):
    Str1 = getParamValue(context,Str1.strip())
    Str2 = getParamValue(context,Str2.strip())
    assert_that(Str1, equal_to_ignoring_case(Str2))

def dowithStr(context,myStr):
    pageID = getParamValue(context,"$pageid")
    if "page_id" in str(myStr):
        #print(myStr)
        index1 =  myStr.find("page_id")
        index2 =  myStr.find(":", index1)
        index3 =  myStr.find(",", index2)
        if index3 == -1:
            index3 =  myStr.find("}", index2)
        #print(myStr[0:index2] +":"+"\""+pageID+"\""+myStr[index3:len(myStr)])
        return  myStr[0:index2] +":"+"\""+pageID+"\""+myStr[index3:len(myStr)]

    else:
        return myStr
