# -*- coding: utf-8 -*-
'''
@author: redstar
'''
import json
import time
import urllib

import requests


_GET = "GET"
_POST = "POST"


class Request():

    def __init__(self, url, params={}, headers={}, data={}, method=_GET, verify=False, allow_redirects=False):
        self.url = url
        self.params = params
        self.headers = headers
        self.data = data
        self.method = method
        self.verify = verify
        self.allow_redirects = allow_redirects
        self.response = {
            'http_status': None,
            'body': {},
            'headers': {}
        }

    def __repr__(self):
        return '<SendRequest %r %r %r %r>' % (self.method, self.url, self.params, self.headers)

    def send_request(self, timeout=60.0, max_try=3):
        print("+++++++++++++++++++++++++++++Sending Request+++++++++++++++++++++++++++++\n")
        timestamp = 0
        max_try = 3
        while(max_try > 0):
            try:
                start = time.time()
                response = self.urlopen(timeout)
                timestamp = time.time() - start

                self.response['http_status'] = response.status_code
                self.response['headers'] = response.headers
                self.response['body'] = response.text
                self.response['history'] = response.history
                break

            except:
                print("[Timeout]Got Exception Try Again...\n[URL] %s" % (self.url + urllib.parse.urlencode(self.params)))
                max_try -= 1

        if max_try <= 0:
            raise Exception("Send http request timeout! Retry failed!")

        #print "[URL] %s\n[Http Status] %s\t[Time Stamp] %s\n[Head] %s\n[Body] %s" % (response.url, response.status_code,
         #                                                                            timestamp, response.headers, response.text)
        #for redirect in self.response['history']:
            #print "[Redirect History] %s\t[Http Status] %s" % (redirect.url, redirect.status_code)

        return self.response

    def urlopen(self, timeout):
        assert self.method in (_GET, _POST)

        if _GET == self.method:
            print("Get数据: "+self.url)
            myheaders = self.headers
            return requests.get(self.url, params=self.params, headers=self.headers, verify=self.verify,
                                allow_redirects=self.allow_redirects, timeout=timeout)
        elif _POST == self.method:
            #return requests.post(self.url, data=json.dumps(self.data), params=self.params, headers=self.headers, verify=self.verify,
            #                     allow_redirects=self.allow_redirects, timeout=timeout)
            print("Post数据: " + str(urllib.parse.urlencode(self.data)))
            myheaders = self.headers
            myheaders["Content-Type"] = "application/x-www-form-urlencoded; charset=UTF-8"
            return requests.post(self.url, data=self.data, params=self.params, headers=myheaders, verify=self.verify,
                                  allow_redirects=self.allow_redirects, timeout=timeout)
