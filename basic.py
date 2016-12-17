# -*- coding: utf-8 -*-
# filename: basic.py
import urllib
import time
import json
import requests
import threading

class Basic:
    def __init__(self):
        self.__accessToken = ''
        self.__leftTime = 0
        self.__accessCount = 0
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()                                  # Start the execution
        
    def __real_get_access_token(self):
        appId = "wxbbe1149cd87deb8b"
        appSecret = "b70777f637696349eff319588dfc1f54"

        self.__accessCount+=1
        print "Get Access Token! Access Count: "+str(self.__accessCount)

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
        getUrl=("https://api.weixin.qq.com/cgi-bin/user/info?access_token=%s&openid=%s&lang=en" % (self.get_access_token(),openid))
        urlResp = urllib.urlopen(getUrl)
        urlResp = json.loads(urlResp.read())
        return urlResp

    def get_user_nickname(self,openid):
        jsonData=self.__get_user_info_json(openid)
        return jsonData['nickname']

    def send_message(self,jsonString):
        postUrl = ("https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token=%s") % (self.get_access_token())
        response = requests.post(postUrl, data=jsonString)
        result = response.json()
        return result['errcode'] == 0 and result['errmsg'] == 'ok'

    def run(self):
        while(True):
            if self.__leftTime > 10:
                time.sleep(2)
                self.__leftTime -= 2
            else:
                self.__real_get_access_token()