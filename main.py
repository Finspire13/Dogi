# -*- coding: utf-8 -*-
# filename: main.py
import web
from handle import Handle
from ferrariInfo import FerrariInfo
import globalData
import terminal
import sys

urls = (
    '/wx', 'Handle',
    '/ferrari', 'FerrariInfo',
)

globalData.initData()

if __name__ == '__main__':
    web.config.debug = True
    app = web.application(urls, globals())
    app.run()