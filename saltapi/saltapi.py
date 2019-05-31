import urllib
import time
import requests


try:
    import json
except ImportError:
    import simplejson as json


try:
    import cookielib
except:
    import http.cookiejar as cookielib

import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context



class SaltAPI(object):

    def __init__(self,url,username,password):
        self.url = url
        self.username = username
        self.password = password
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",
            'Content-type': 'application/json',
        }
        self.params = {'client': 'local','fun': '','tgt': ''}
        self.login_url=self.url + 'login'
        self.login_params = {'username': self.username,'password': self.password,'eauth': 'pam'}
        self.token=self.get_data(self.login_url,self.login_params)['token']
        self.__token_id = self.token
        self.headers['X-Auth-Token'] = self.token

    def get_data(self,url,params):
        send_data = json.dumps(params)
        request = requests.post(url,data=send_data,headers=self.headers,verify=False)
        response = request.json()
        result = dict(response)
        return result['return'][0]



    def salt_command(self,tgt,method,arg=None):
        if arg:
            params = {'client': 'local','fun': method, 'tgt': tgt,'arg': arg}
        else:
            params = {'client': 'local','fun': method, 'tgt': tgt}

        result = self.get_data(self.url,params)
        return result

