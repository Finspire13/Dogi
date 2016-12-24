# -*- coding: utf-8 -*-
# filename: handle.py

import hashlib
from reply import ReplyMessage
from receive import ReceiveMessage
import web
from terminal import process
from connection import connection
import traceback


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
            web_data = web.data()
            print web_data
            if len(web_data) == 0:
                return "success"
            receive_message = ReceiveMessage(web_data)
            if receive_message and receive_message.message_type == 'text':
                to_user = receive_message.from_user_name
                from_user = receive_message.to_user_name
                received_content = receive_message.content
                contents = process(to_user, received_content)
                connection.me = from_user
                success = 0
                for content in contents:
                    reply_message = ReplyMessage(to_user, from_user, content, 'text')
                    #print reply_message.get_json()
                    success += connection.send_message(reply_message.get_json())
                if success == 0:
                    return "success"
                else:
                    return
            else:
                return "success"
        except Exception, Argument:
            #print str(Exception)
            #print Argument
            traceback.print_exc() 
            return Argument
