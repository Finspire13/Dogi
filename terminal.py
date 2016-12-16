# -*- coding: utf-8 -*-
# filename: terminal.py
from basic import Basic
import globalData

class Terminal(object):

	def process(self,fromUserName,content):
		if fromUserName in globalData.activeUserSet:
			if content == "shutdown":
				globalData.activeUserSet.remove(fromUserName)
				result = "Bye, "+Basic().get_user_nickname(fromUserName)
				result = result.encode('utf-8')
				return result
			return fromUserName+" "+content #to do
		else:
			if content == "Dogi-70":
				globalData.activeUserSet.add(fromUserName)
				result = "Welcome, "+Basic().get_user_nickname(fromUserName)
				result = result.encode('utf-8')
				return result
			else:
				return "Enter 'Dogi-70' to activate its terminal."


