# -*- coding: utf-8 -*-
# filename: handle.py
import hashlib
import reply
import receive
import web
import globalData
from terminal import Terminal
from basic import Basic

class Handle(object):

    def GET(self):
        try:
            data = web.input()
            if len(data) == 0:
                return "hello, this is handle view, data = 0"
            signature = data.signature
            timestamp = data.timestamp
            nonce = data.nonce
            echostr = data.echostr
            token = "dogi_access"

            list = [token, timestamp, nonce]
            list.sort()
            sha1 = hashlib.sha1()
            map(sha1.update, list)
            hashcode = sha1.hexdigest()
            print "handle/GET func: hashcode, signature: ", hashcode, signature
            if hashcode == signature:
                return echostr
            else:
                return ""
        except Exception, Argument:
            return Argument


    def POST(self):
        try:
            webData = web.data()
            print "Handle Post webdata is ", webData
            recMsg = receive.parse_xml(webData)
            if isinstance(recMsg, receive.Msg) and recMsg.MsgType == 'text':
                toUser = recMsg.FromUserName
                fromUser = recMsg.ToUserName
                receivedContent = recMsg.Content
                contents = Terminal().process(recMsg.FromUserName,receivedContent)

                successFlag = True
                #print contents
                for content in contents:
                    replyMsg = reply.TextMsg(toUser, fromUser, content)
                    #print replyMsg.sendJSON()
                    tempFlag = globalData.wechatBasic.send_message(replyMsg.sendJSON())
                    if not tempFlag:
                        successFlag = False

                if successFlag:
                    return "success"
                else:
                    return
            else:
                print "Ignored"
                return "success"
        except Exception, Argment:
            return Argment