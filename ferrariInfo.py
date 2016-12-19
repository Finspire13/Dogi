# -*- coding: utf-8 -*-
# filename: ferrariInfo.py

import web

class FerrariInfo(object):
	def GET(self):
		content = ("Donald Ferrari\n\n"+
				"Background:\n"+
				"1994-1999, Researcher at Carnegie Mellon University, USA\n"+
				"1999-2001, Joint Laboratory of Intelligent Informatic, Switzerland\n"+
				"2002-2006, Advanced Researcher at Ginne Inc.\n"+
				"2006-, It's hard to say...\n\n"
				"Publication:\n"+
				"'Reliability Analysis of Intelligence System.'\n"+
				"'Principles of Intelligent Agent'\n"+
				"'Multi-directional Interconnected Intelligent Terminals'\n"
				"...\n\n"+
				"...")
		return content