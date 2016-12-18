import time
import requests
import json

class Configs:
    def __init__(self):
        #hard coded configuration
        self.app_id = "wxbbe1149cd87deb8b"
        self.app_secret = "b70777f637696349eff319588dfc1f54"
        self.api_url = "https://api.weixin.qq.com/cgi-bin"
        self.access_token = None
        self.timer = time.time()

settings = Configs()
