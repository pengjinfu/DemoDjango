# /*********************************************
# *  使用django 框架
# *  使用request 来请求接口获取数据
# *********************************************/
import base64
import hashlib
import sys

import logging
import requests

## 引入类的操作，
import json
import pandas as pd
import time
from pandas import DataFrame


def get_weather():
    url = 'http://t.weather.sojson.com/api/weather/city/101030100'
    ori = requests.get(url)
    data = ori.json()
    return data


def get_token_alg(advertiser_id, app_key, app_id):
    t = int(time.time())
    sign = hashlib.sha1((str(t) + str(advertiser_id) + app_key).encode("utf-8")).hexdigest()
    token = base64.b64encode(bytes("{},{},{},{}".format(t, advertiser_id, app_id, sign), encoding="utf8"))
    return token


def get_token(advertiser_id):
    app_id = 3
    advertiser_id = 763
    app_key = 'SqQZ%&ew9!2DDQUjee'
    token = get_token_alg(advertiser_id, app_key, app_id)
    return token


def get_code_list():
    url = "http://dev2.user.kuaizi.co/advertise/Project/queryProjectList"
    data = api(url, None, method_type='get')
    return data


def api(url, params, method_type='get'):
    token = 'eNortjI2s1IyScouSktKKcpOLSwuTU1PNytLMSjLMynJz1c2NzNWNlwwQSVrXDBL2Q2j'
    headers = {'content-type': 'application/json', "token": token}
    if str.lower(method_type) == 'get':
        respone = requests.get(url, params=params, headers=headers)
    else:
        respone = requests.post(url, params=params, headers=headers)
    result = respone.text
    if result != None and len(result) > 0:
        try:
            data = json.loads(s=result)
            return data
        except ValueError:
            return None
    return None


#
# def send_email(to, subject, message, advertiser_id):
#     app_id = 3
#     app_key = 'SqQZ%&ew9!2DDQUjee'
#     token = get_token(advertiser_id)
#     url = "http://dev.api.kuaizitech.com/service/send_email/send"
#     headers = {'content-type': 'application/json', "token": token}
#     data = {
#         "to": to,
#         "subject": subject,
#         "message": message
#     }
#     ret = requests.post(url, json=data, headers=headers)
#     print(ret.text)
#     logging.info(ret.text)


def parse_params(param_str):
    '''
    对参数的raw 格式解析
    描述：
    1. 每个参数和值作为一行
    2. 参数的分割采用‘:’来处理
    3. 对于解析的参数为空的情况，自动使用空格符号默认，如 ''
    4. 解析返回的数据是数组/dict格式

    例子：
    project_id: 2750299
    start_date: 2018-10-09
    end_date: 2018-10-15

    '''

    params = {}
    if param_str is not None and len(param_str) > 0:
        param_arr = str.split(param_str, '\n')
        if len(param_arr) > 0:
            for value in param_arr:
                value = str.strip(value)
                if value is not None and len(value) > 0:
                    param = str.split(value, ':')
                    if len(param) < 2:
                        params[str.strip(param[0])] = ''
                    else:
                        params[str.strip(param[0])] = str.lstrip(param[1])

            return params
    return params


def get_campaign_list():
    param_str = '''
        project_id: 2750299
        start_date: 2018-10-09
        end_date: 2018-10-15
        creative_type: banner
        platform_id: 151
        ad_set_id:
        campaign_id:
        campaign_state:
        kpi_status:
        order_field:
        order_type:
        page: 1
        page_size: 10
        index: impression_num,click_num,click_ratio,charge,cpc,cpm,uv,link_click,inline_link_clicks
    '''
    params = parse_params(param_str)
    print(type(params))
    url = "http://dev.user.kuaizi.co/report/v2.Campaign/queryCampaignStatisticsList"
    data = api(url, params)
    print(data)
    return data


if __name__ == "__main__":
    # weather_json = get_weather()
    # print({'time': weather_json['time'], 'cityInfo': weather_json['cityInfo']})
    # data = get_code_list()
    # df = DataFrame(data['data']['list'])
    # print(df)

    #     param_str = '''
    #        project_id: 2750299
    # start_date: 2018-10-09
    # end_date: 2018-10-15
    # creative_type: banner
    # platform_id: 151
    # ad_set_id:
    # campaign_id:
    # campaign_state:
    # kpi_status:
    # order_field:
    # order_type:
    # page: 1
    # page_size: 10
    # index: impression_num,click_num,click_ratio,charge,cpc,cpm,uv,link_click,inline_link_clicks
    #     '''
    #     params = parse_params(param_str)
    #     print(params)

    data = get_campaign_list()
