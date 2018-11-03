from CAL.PyCAL import *
import pandas as pd
import numpy as np
import talib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.patches as patches

## 参数的基本配置：时间段，交易信息
start = '2018-01-01'
end = '2018-09-05'
# ID = '000014.XSHE'
# ID = '000014.XSHE'
# ID = '600446.XSHG'
# MAX_DIF = 0.03 # 效果比较好
MAX_DIF = 0.02

# XSHG,XSHE,CCFX,XDCE,XSGE,XZCE,XHKG。XSHG表示上海证券交易所,XSHE表示深圳证券交易所,CCFX表示中国金融期货交易所,XDCE表示大连商品交易
IDS = ['002661.XSHE', '600446.XSHG']
start = Date.strptime(start, dateFormat='%Y-%m-%d')
cal = Calendar('China.SSE')
dt_new = cal.advanceDate(start, '-100B', BizDayConvention.Following)


# data1 =  DataAPI.MktEqudAdjGet(secID=ID, beginDate=start, endDate=end, isOpen='1',field=["secShortName","ticker","openPrice","closePrice","highestPrice","lowestPrice","tradeDate","turnoverRate","isOpen"])

## 计算MACD的数据值
# dif,dea,macd = talib.MACD(data1['closePrice'].values, fastperiod=12, slowperiod=26, signalperiod=9)

def plot_k(ID, beginDate, endDate, Type='d'):
    '''
       绘制K线，包括均线， 交易量， MACD图
       1. 绘制“蜡烛图” + 均线配置
       2. 显示交易量图和交易量均线
       3. 显示MACD的DIF, DEA， MACD的数值计算
         DIF线：　（Difference）短期EMA和长期EMA的离差值
         DEA线：　（Difference Exponential Average）DIF线的M日
       4. 新增一条曲线：标注买卖信号

    '''
    cal = Calendar('China.SSE')

    ## 小时维度
    if Type == 'h':
        quotes = DataAPI.MktEqudAdjGet(secID=ID, beginDate=beginDate, endDate=endDate, isOpen='1',
                                       field=["secShortName", "ticker", "openPrice", "closePrice", "highestPrice",
                                              "lowestPrice", "tradeDate", "turnoverRate", "isOpen"])
        dt_new = cal.advanceDate(beginDate, '-100B', BizDayConvention.Following)
        quotes2 = DataAPI.MktEqudAdjGet(secID=ID, beginDate=dt_new, endDate=endDate, isOpen='1',
                                        field=["secShortName", "ticker", "openPrice", "closePrice", "highestPrice",
                                               "lowestPrice", "tradeDate", "turnoverRate", "isOpen"])

    ## 天维度
    elif Type == 'd':
        quotes = DataAPI.MktEqudAdjGet(secID=ID, beginDate=beginDate, endDate=endDate, isOpen='1',
                                       field=["secShortName", "ticker", "openPrice", "closePrice", "highestPrice",
                                              "lowestPrice", "tradeDate", "turnoverRate", "isOpen"])
        dt_new = cal.advanceDate(beginDate, '-100B', BizDayConvention.Following)
        quotes2 = DataAPI.MktEqudAdjGet(secID=ID, beginDate=dt_new, endDate=endDate, isOpen='1',
                                        field=["secShortName", "ticker", "openPrice", "closePrice", "highestPrice",
                                               "lowestPrice", "tradeDate", "turnoverRate", "isOpen"])
    ## 周维度
    elif Type == 'w':
        quotes = DataAPI.MktEquwAdjGet(secID=ID, beginDate=beginDate, endDate=endDate, isOpen='1',
                                       field=["secShortName", "ticker", "openPrice", "closePrice", "highestPrice",
                                              "lowestPrice", "tradeDate", "turnoverRate", "isOpen"])
        quotes['tradeDate'] = range(0, len(quotes.index))
        dt_new = cal.advanceDate(beginDate, '-100w', BizDayConvention.Following)
        quotes2 = DataAPI.MktEquwAdjGet(secID=ID, beginDate=dt_new, endDate=endDate, isOpen='1',
                                        field=["secShortName", "ticker", "openPrice", "closePrice", "highestPrice",
                                               "lowestPrice", "tradeDate", "turnoverRate", "isOpen"])
        quotes2['tradeDate'] = range(0, len(quotes2.index))

    ## 月维度
    elif Type == 'm':
        quotes = DataAPI.MktEqumAdjGet(secID=ID, beginDate=beginDate, endDate=endDate, isOpen='1',
                                       field=["secShortName", "ticker", "openPrice", "closePrice", "highestPrice",
                                              "lowestPrice", "tradeDate", "turnoverRate", "isOpen"])
        quotes['tradeDate'] = range(0, len(quotes.index))
        dt_new = cal.advanceDate(beginDate, '-100m', BizDayConvention.Following)
        quotes2 = DataAPI.MktEqumAdjGet(secID=ID, beginDate=dt_new, endDate=endDate, isOpen='1',
                                        field=["secShortName", "ticker", "openPrice", "closePrice", "highestPrice",
                                               "lowestPrice", "tradeDate", "turnoverRate", "isOpen"])
        quotes2['tradeDate'] = range(0, len(quotes2.index))

    ## 计算MACD的数据值，并分别显示dif,dea,macd 的数据列表信息
    dif, dea, macd = talib.MACD(quotes2['closePrice'].values, fastperiod=12, slowperiod=26, signalperiod=9)
    # print([dif,dea,macd ])

    __color_balck__ = '#000000'
    __color_green__ = '#00FFFF'
    __color_purple__ = '#9900CC'
    __color_golden__ = '#FFD306'

    ## 设置画图的布局
    fig = plt.figure(figsize=(13.5, 5))
    fig.set_tight_layout(True)

    ## 现在背景色，标题
    ax1 = fig.add_axes([0, 1, 1, 1], axis_bgcolor='w')
    ax1.set_title(quotes.ix[0, 'tradeDate'])
    ax1.set_axisbelow(True)
    ax2 = fig.add_axes([0, 0.6, 1, 0.25], axis_bgcolor='w')
    ax2.set_axisbelow(True)
    ax1.grid(True)
    ax2.grid(True)
    ax1.set_xlim(-1, len(quotes) + 1)
    ax2.set_xlim(-1, len(quotes) + 1)
    ax3 = fig.add_axes([0, 0.10, 1, 0.25], axis_bgcolor='w')
    ax3.set_xlim(-1, len(quotes) + 1)

    ## 买入或者卖出的信号数据
    singal = []
    singal_tmp = []

    ##  对交易列表的数据进行处理，并渲染其数据
    for i in range(len(quotes)):
        close_price = quotes.ix[i, 'closePrice']
        open_price = quotes.ix[i, 'openPrice']
        high_price = quotes.ix[i, 'highestPrice']
        low_price = quotes.ix[i, 'lowestPrice']
        vol = quotes.ix[i, 'turnoverRate']
        trade_date = quotes.ix[i, 'tradeDate']

        # 获取macd每个点的值
        Macd = macd[-len(quotes) + i]
        tmpDif = dif[-len(quotes) + i]
        tmpDea = dea[-len(quotes) + i]

        # 对于存在极值的情况，作为信号的进行标注,误差在百分之一以内 @todo
        if abs(tmpDif - tmpDea) <= MAX_DIF:
            singal.append(tmpDif)
            singal_tmp.append({'tradeDate:': trade_date, 'dif_value:': tmpDif})
        else:
            singal.append(0)

        # 收盘大于开盘，表示增长，使用红线绘制曲线
        if close_price > open_price:
            ax1.add_patch(
                patches.Rectangle((i - 0.35, open_price), 0.7, close_price - open_price, fill=True, color='r'))
            ax1.plot([i, i], [low_price, open_price], 'r')
            ax1.plot([i, i], [close_price, high_price], 'r')
            ax2.add_patch(patches.Rectangle((i - 0.35, 0), 0.7, vol, fill=True, color='r'))

        # 收盘小于或等于开盘，表示均衡或者下降，使用绿先绘制曲线
        else:
            ax1.add_patch(patches.Rectangle((i - 0.35, open_price), 0.7, close_price - open_price, color='g'))
            ax1.plot([i, i], [low_price, high_price], color='g')
            ax2.add_patch(patches.Rectangle((i - 0.35, 0), 0.7, vol, color='g'))

        # 如果macd值大于0，则显示红色，否则显示绿色
        if Macd >= 0:
            ax3.add_patch(patches.Rectangle((i - 0.35, 0), 0.7, Macd, color='r'))
        else:
            ax3.add_patch(patches.Rectangle((i - 0.35, Macd), 0.7, -Macd, color='g'))

    print(singal_tmp)
    ## 分别渲染标题，标签，包括 K线（ax1），交易量(ax2)，MACD的曲线(ax3)
    ax1.set_title(quotes['secShortName'][1].decode('utf-8'), fontproperties=font, fontsize=15, loc='left', color='r')
    ax2.set_title(u'成交量', fontproperties=font, fontsize=15, loc='left', color='r')
    ax3.set_title(u'MACD指标', fontproperties=font, fontsize=15, loc='left', color='r')
    ax1.set_xticks(range(0, len(quotes), 15))
    ax2.set_xticks(range(0, len(quotes), 15))
    ax3.set_xticks(range(0, len(quotes), 15))

    s1 = ax1.set_xticklabels([quotes.ix[index, 'tradeDate'] for index in ax1.get_xticks()])
    s1 = ax2.set_xticklabels([quotes.ix[index, 'tradeDate'] for index in ax2.get_xticks()])
    s3 = ax3.set_xticklabels([quotes.ix[index, 'tradeDate'] for index in ax3.get_xticks()])

    ## 使用的均线包括：5日，10日，20日，96日均线，@todo，这个均线需要根据实际情况配置下
    ma5 = pd.rolling_mean(np.array(quotes2['closePrice'], dtype=float), window=5, min_periods=0)[-len(quotes):]
    ma10 = pd.rolling_mean(np.array(quotes2['closePrice'], dtype=float), window=10, min_periods=0)[-len(quotes):]
    ma20 = pd.rolling_mean(np.array(quotes2['closePrice'], dtype=float), window=20, min_periods=0)[-len(quotes):]
    ma96 = pd.rolling_mean(np.array(quotes2['closePrice'], dtype=float), window=96, min_periods=0)[-len(quotes):]

    ## 绘制不同的展示类型的不同均线
    ax1.plot(ma5, color='b')
    ax1.plot(ma10, color='y')
    ax1.plot(ma20, color=__color_purple__)
    ax1.plot(ma96, color=__color_golden__)

    ax1.annotate('MA5-', xy=(len(quotes) - 32, ax1.get_yticks()[-1]), color='b', fontsize=10)
    ax1.annotate('MA10-', xy=(len(quotes) - 24, ax1.get_yticks()[-1]), color='y', fontsize=10)
    ax1.annotate('MA20-', xy=(len(quotes) - 16, ax1.get_yticks()[-1]), color=__color_purple__, fontsize=10)
    ax1.annotate('MA96-', xy=(len(quotes) - 8, ax1.get_yticks()[-1]), color=__color_golden__, fontsize=10)

    ax3.annotate('DIF-', xy=(len(quotes) - 32, ax3.get_yticks()[-1]), color='r', fontsize=10)
    ax3.annotate('DEA-', xy=(len(quotes) - 24, ax3.get_yticks()[-1]), color='y', fontsize=10)
    ax3.annotate('SINGAL-', xy=(len(quotes) - 16, ax3.get_yticks()[-1]), color=__color_purple__, fontsize=10)

    ## 绘制交易量图
    vol5 = pd.rolling_mean(np.array(quotes['turnoverRate'], dtype=float), window=5, min_periods=0)
    vol10 = pd.rolling_mean(np.array(quotes['turnoverRate'], dtype=float), window=10, min_periods=0)
    ax2.plot(vol5, color='b')
    ax2.plot(vol10, color='y')

    ## 绘制MACD的图信息
    ax3.plot(dif[-len(quotes):], color='r')
    ax3.plot(dea[-len(quotes):], color='y')
    ax3.plot(singal[-len(quotes):], color=__color_purple__)
    return fig


for secId in IDS:
    # plot_k('000014.XSHE', Date.todaysDate()-Period('150d'), Date.todaysDate(),Type='d')
    print(secId)
    plot_k(secId, Date.todaysDate() - Period('150d'), Date.todaysDate(), Type='d')
    # print(secId)

# plot_k('000014.XSHE', Date.todaysDate()-Period('150d'), Date.todaysDate(),Type='w')
# plot_k('000014.XSHE', Date.todaysDate()-Period('150d'), Date.todaysDate(),Type='m')


