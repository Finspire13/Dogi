# -*- coding: utf-8 -*-
# filename: terminal.py
from basic import Basic
import random
import globalData

class Terminal(object):

	def __inner_process(self,content):
		#print 9
		return {
			"help":("These commands are defined internally:\n\n"+
				"info [subject]\n"+
				"<Get information about the subject.>\n\n"+
				"list [option]\n"+
				"<Get file list. Specify maximum files to show on screen. Latest ones will be shown. '-a' for all files.>\n\n"+
				"open [filename]\n"+
				"<Open file>\n\n"+
				"shutdown\n"+
				"<Shut down the terminal.>"),

			"list":("0x0089AB readme 20161211\n"+
				"0x01000D File Missing\n"+
				"0x00C000 File Missing\n"+
				"0x0F9090 File Missing\n"+
				"0x011115 File Missing\n"+
				"0x0843C4 File Missing\n"),

			"info Dogi":("Dogi series is an advanced AI system in development.\n\n"+
				"Dogi with its full ability will promise human a brave new world.\n\n"+
				"The main contributor to Dogi is Dr.Ferrari. Dogi is supported by Ginne Inc."),

			"info Mr.Dog":"A great man",

			"info Dr.Ferrari":("Donald Ferrari is an American computer scientist."+
				" He is the author of the multi-volume work Principles of Intelligent Agent."+
				" He contributed to the development of highly-reliable AI system.\n"+
				"Personal website: 123.206.179.29/ferrari"),

			"info Ginne":("Ginne is an multinational technology company with the vision of reducing the 'risk of human extinction' "+
				"and conducting space exploration."),

			"info Ginne Inc.":("Ginne is an multinational technology company with the vision of reducing the 'risk of human extinction' "+
				"and conducting space exploration."),

			"info RAIRC":("Robots and Artificial Intelligence Regulatory Commission (RAIRC) "+
				"is an international agency tasked with protecting public safety against misuse of AI and robots."+
				"RAIRC was established in 2015 as a result of Shanghai Protocol."),

			"info Shanghai Protocol": "Missing",

			"open readme":("Something dangerous is hidden in this system and you must find it.\n\n"+
				"Dogi terminals are synced with Dogi Cloud Server. You need to check Dogi for every update.\n\n"+
				"Good Luck.\n\n"+
				"EOF")

		}.get(content,"Command Not Found")


	def process(self,fromUserName,content):

		if fromUserName in globalData.activeUserDict:
			if globalData.activeUserDict[fromUserName] == 'Started':
				if content == "human":
					globalData.activeUserDict[fromUserName] = 'Logged In'
					result1 = "Identifying...Success."
					result2 = "Welcome, "+Basic().get_user_nickname(fromUserName)+"\nType [help] for help."
					result2 = result2.encode('utf-8')
					resultList = [result1,result2]
					return resultList
				elif content == "AI":
					globalData.activeUserDict.pop(fromUserName)
					result1 = "Authenticating..."
					result2 = ("Permission Denied: \nAI Unregistered with RAIRC.\n"+
						"------------------\n"+
						"Terminal shutting down.")
					resultList = [result1,result2]
					return resultList
				else:
					globalData.activeUserDict.pop(fromUserName)
					result1 = ("Permission Denied: \nInvalid response.\n"+
						"------------------\n"+
						"Terminal shutting down.")
					resultList = [result1]
					return resultList

			elif globalData.activeUserDict[fromUserName] == 'Logged In':
				if content == "shutdown":
					#print 3
					globalData.activeUserDict.pop(fromUserName)
					#print globalData.activeUserSet
					result1 = "Logged out, "+Basic().get_user_nickname(fromUserName)
					result1 = result1.encode('utf-8')
					result2 = ("Shutting Down\n"+
						"=============>100%\n"+
						"Finished.")
					resultList = [result1,result2]
					return resultList
				#to improve
				else:
					#print 4
					resultList=[self.__inner_process(content)]
					return resultList
		else:
			if content == "Dogi":
				globalData.activeUserDict[fromUserName] = 'Started'
				result1 = ("Dogi Instance #"+ str(int(random.random()*70+30)) +"\nVersion 1.0.2\n"+
					"==============>100%\n"+
					"Terminal Started.")
				result2 = "Are you human or AI? [human/AI]"
				resultList = [result1, result2]
				return resultList
			else:
				resultList = ["Enter 'Dogi' to activate its terminal."]
				return resultList
