import numpy as np
import scipy.stats as stats
import scipy.optimize as opt
import pandas as pd

from pandas import Series


def st_numpy():
    a = np.random.rand(5)
    print(a)

    b = np.array([[3.2, 1.5], [2.5, 4]])
    c = b.copy()
    print(b)
    print(c)

    a = np.random.rand(2, 4)
    print("a:")
    print(a)

    a = np.transpose(a)
    print("traspose(a)")
    print(a)

    b = np.mat(b)
    print("")
    print(b)

    print('hstack---------------')

    a = np.random.rand(2, 2)
    b = np.random.rand(2, 2)
    c = np.hstack([a, b])
    print(c)
    d = np.vstack([a, b])
    print(d)

    print('nan---------------')

    a[0, 1] = np.nan
    print(a)
    print(np.isnan(a))


if __name__ == '__main__':
    # st_numpy()

    '''
      统计学的库scipy库
      使用统计学里面的的方式和方法来处理逻辑
      1. 随机的分布逻辑

      数据处理的瑞士军刀pandas
      1. Series 类似hash的dict,一般是一维度


    '''
    s = Series(np.random.randn(5), index=['a', 'b', 'c', 'd', 'e'])
    print(s)
    print(s[0:2])
    print(s['b'])
    print(s['e'])

    print('pandas----------------')
    print(pd.__version__)

    d = {'one': Series([1., 2., 3.], index=['a', 'b', 'c']),
         'two': Series([1., 2., 3., 4.], index=['a', 'b', 'c', 'd'])}
    df = pd.DataFrame(d)
    print(df)

    print('pandas->data frame----------------')
    df = pd.DataFrame()
    index = ['alpha', 'beta', 'gamma', 'delta', 'eta']
    for i in range(5):
        a = pd.DataFrame([np.linspace(i, 5 * i, 5)], index=[index[i]])
        df = pd.concat([df, a], axis=0)

    print(df)
    print(df[1])
    print(type(df[1]))
    print(df[1]['beta'])
    print('pandas->data frame ->at ----------------')
    print(df)
    print(df.iat[2, 3])

    print('pandas->date_range----------------')
    dates = pd.date_range('20150101', periods=5)
    print(dates)

    df = pd.DataFrame(np.random.randn(5, 4), index=dates, columns=list('ABCD'))
    print(df)
    print(df.head())
    print(df.tail(3))
    print(df.describe())

    print("Order by column names----------------------")
    print(df.sort_index)

    print("pandas->stock_list")
    stock_list = ['000001.XSHE', '000002.XSHE', '000568.XSHE', '000625.XSHE', '000768.XSHE', '600028.XSHG',
                  '600030.XSHG', '601111.XSHG', '601390.XSHG ', '601998.XSHG']

    stock_list = ['000001.XSHE', '000002.XSHE', '000568.XSHE', '000625.XSHE', '000768.XSHE', '600028.XSHG',
                  '600030.XSHG', '601111.XSHG', '601390.XSHG ', '601998.XSHG']

    raw_data = DataAPI.MktEqudGet(secID=stock_list, beginDate='20150101', end
    Date = '20150131', pandas = '1')
    df = raw_data[['secID', 'tradeDate', 'secShortName', 'openPrice', 'highes tPrice', 'lowestPrice', 'closePrice',
                   'turnoverVol']]
    print(df)
