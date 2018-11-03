from CAL.PyCAL import *
import pandas as pd
import numpy as np
import talib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.patches as patches

## 参数的基本配置：时间段，交易信息
start = '20150513'
end = '20180905'
# ID = '000014.XSHE'
# ID = '000014.XSHE'
# ID = '600446.XSHG'
# ID = '002871.XSHE' # 伟隆股份
# ID = '601225.XSHE' # 陕西煤业
# MAX_DIF = 0.03 # 效果比较好
MAX_DIF = 0.1
ID = 'cu9999.CCFX'

quotes2 = DataAPI.MktMFutdGet(mainCon=u"1",contractMark=u"",contractObject=u"I",tradeDate=u"20180605",startDate=u"",endDate=u"",field=u"secID,ticker,secShortName,tradeDate,openPrice,closePrice,highestPrice,lowestPrice",pandas=“1”)

print(quotes2)

quotes = DataAPI.MktFutwGet(secID="",ticker="cu9999",beginDate="20150513",endDate="20180513",field=["secShortName","ticker","openPrice","closePrice","highestPrice","lowestPrice","turnoverRate","isOpen"],pandas="1")

print(quotes)


# # XSHG,XSHE,CCFX,XDCE,XSGE,XZCE,XHKG。XSHG表示上海证券交易所,XSHE表示深圳证券交易所,CCFX表示中国金融期货交易所,XDCE表示大连商品交易

# quotes = DataAPI.MktFutwGet(ID,ticker='cu1106', beginDate=start, endDate=end,field=["openPrice"],pandas="1")
# print(quotes)


