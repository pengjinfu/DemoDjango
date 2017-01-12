# -*- coding: utf-8 -*-
'''
@author: wilson
'''
import time
from features.steps.config import *
from hamcrest import *  # @UnusedWildImport
import json

def praseStrToDic(param):
    strS = param.split("&")
    data = {}
    for tmpStr in strS:
        pTemp = tmpStr.split("=")
        data[pTemp[0]] = pTemp[1]
    return data

def datetime_timestamp(dt):
     #dt为字符串
     #中间过程，一般都需要将字符串转化为时间数组
     time.strptime(dt, '%Y-%m-%d %H:%M:%S')
     ## time.struct_time(tm_year=2012, tm_mon=3, tm_mday=28, tm_hour=6, tm_min=53, tm_sec=40, tm_wday=2, tm_yday=88, tm_isdst=-1)
     #将"2012-03-28 06:53:40"转化为时间戳
     s = time.mktime(time.strptime(dt, '%Y-%m-%d %H:%M:%S'))
     return str(int(s))


def timestamp_datetime(value,format = '%Y-%m-%d %H:%M:%S'):
    # value为传入的值为时间戳(整形)，如：1332888820
    value = time.localtime(value)
    ## 经过localtime转换后变成
    ## time.struct_time(tm_year=2012, tm_mon=3, tm_mday=28, tm_hour=6, tm_min=53, tm_sec=40, tm_wday=2, tm_yday=88, tm_isdst=0)
    # 最后再经过strftime函数转换为正常日期格式。
    dt = time.strftime(format, value)
    return dt

def assertNumber(sourceNum,targetNum,name = ""):
    tagetNumFormat = abs(targetNum)
    MatcheRateTmp = 0
    if tagetNumFormat<= 10:
        MatcheRateTmp = float(MatcheRate["1"])
    elif tagetNumFormat<=100 and tagetNumFormat>10:
        MatcheRateTmp = float(MatcheRate["2"])
    elif tagetNumFormat<=100 and tagetNumFormat>10:
        MatcheRateTmp = float(MatcheRate["2"])
    elif tagetNumFormat<=1000 and tagetNumFormat>100:
        MatcheRateTmp = float(MatcheRate["3"])
    elif tagetNumFormat<=2500 and tagetNumFormat>1000:
        MatcheRateTmp = float(MatcheRate["4"])
    elif tagetNumFormat<=5000 and tagetNumFormat>2500:
        MatcheRateTmp = float(MatcheRate["5"])
    elif tagetNumFormat<=10000 and tagetNumFormat>5000:
        MatcheRateTmp = float(MatcheRate["6"])
    else:
        MatcheRateTmp = float(MatcheRate["7"])
    if name != "":
        print(name)
    assert_that(sourceNum, close_to(targetNum,abs(targetNum)*MatcheRateTmp))

def getValue(key,dicValue):
    keys = str(key).split(">")
    dicTmp = dicValue
    for item in keys:
        if item is not  None:
            dicTmp = getDicValue(item,dicTmp)
    return  dicTmp

def getDicValue(key,dicValue):
    try:
        valueTmp = json.loads(dicValue, encoding='utf-8')
    except:
        valueTmp = dicValue
    if str(key) == "UNKEY":
        for item in valueTmp.keys():
            return valueTmp[item]
    elif str(key).startswith("$"):
        return  valueTmp[int(str(key).replace("$",""))]
    else:
        return  valueTmp[str(key)]

def getAccountSpend(spend,AccountID):
    if str(AccountID) in AccountExchangeRate:
        return float(spend)*float(AccountExchangeRate[str(AccountID)])
    else:
        return float(spend)

def doWithStr(inStr):
    return str(inStr).replace("$","").replace(",","")