# -*- coding: utf-8 -*-
# filename: main.py
import web
from handle import Handle
import globalData
import terminal

urls = (
    '/wx', 'Handle',
)

globalData.initData()

if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()