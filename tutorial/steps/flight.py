from behave import *

@given('a set of specific users')
def step_impl(context):
    for row in context.table:
        #print([['name'],row['department']]);
        print("a")
        #model.add_user(name=row['name'], department=row['department'])

@given(u'[{httpHost:S}]发送{mode:S}请求--API接口{api:S}')
def send_request(context, httpHost, mode, api,retryNum =0):
    print("bbbb"); exit()