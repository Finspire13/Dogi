# -*- coding: utf-8 -*-
# filename: main.py

import web
from handle import Handle
from ferrariInfo import FerrariInfo

if __name__ == '__main__':

	urls = (
		'/wx', 'Handle',
		'/ferrari', 'FerrariInfo',
		)
	app = web.application(urls, globals())
	app.run()
