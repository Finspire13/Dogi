# -*- coding: utf-8 -*-
# filename: basic.py
import urllib
import time
import json

class Basic:
    def __init__(self):
        self.__accessToken = ''
        self.__leftTime = 0
    def __real_get_access_token(self):
        appId = "wxbbe1149cd87deb8b"
        appSecret = "b70777f637696349eff319588dfc1f54"

        postUrl = ("https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s" % (appId, appSecret))
        urlResp = urllib.urlopen(postUrl)
        urlResp = json.loads(urlResp.read())
        
        self.__accessToken = urlResp['access_token']
        self.__leftTime = urlResp['expires_in']

    def get_access_token(self):
        if self.__leftTime < 10:
            self.__real_get_access_token()
        return self.__accessToken

    def __get_user_info_json(self,openid):
        getUrl=("https://api.weixin.qq.com/cgi-bin/user/info?access_token=%s&openid=%s&lang=en"%(Basic().get_access_token(),openid))
        urlResp = urllib.urlopen(getUrl)
        urlResp = json.loads(urlResp.read())
        return urlResp

    def get_user_nickname(self,openid):
        jsonData=self.__get_user_info_json(openid)
        return jsonData['nickname']

    def run(self):
        while(True):
            if self.__leftTime > 10:
                time.sleep(2)
                self.__leftTime -= 2
            else:
                self.__real_get_access_token()