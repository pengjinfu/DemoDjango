# -*- coding: utf-8 -*-
'''
@author: redstar
'''
from behave import then
from behave import when
from features.utils.http_req import Request
from hamcrest import *  # @UnusedWildImport


def replace_domain_name(url, host):
    return url.replace("net.rayjump.com", host).replace("de.rayjump.com", host)\
        .replace("sg.rayjump.com", host).replace("us.rayjump.com", host)\
        .replace("de.hahamobi.com", host).replace("sg.hahamobi.com", host)\
        .replace("us.hahamobi.com", host).replace("preonline.rayjump.com", host)


@when(u'[Inner]访问{url:S}')
def _send_request(context, url):
    context.response = Request(url).send_request()


@then(u'[Inner]访问url成功,http返回码{code:d}')
def _check_http_code(context, code):
    assert_that(context.response.get("http_status"), is_(code))


@then(u'[Inner]访问url成功,http返回成功')
def _check_http_success(context):
    if ((context.config.userdata["jump"]) == "true" ):
        assert_that(context.response.get("http_status"), is_in([200, 302]))


@then(u'检查CORS跨越标志{cors}')
def check_response_cors(context, cors):
    assert_that(context.response.get("headers"),
                has_entries(eval(cors)), "response headers")
