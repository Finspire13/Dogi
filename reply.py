import time

class ReplyMessage:
    def __init__(self, to_user_name, from_user_name, content, type):
        self.dict = dict()
        self.dict['to_user_name'] = to_user_name
        self.dict['from_user_name'] = from_user_name
        self.dict['create_time'] = int(time.time())
        self.type = type
        if type == 'text':
            self.dict['content'] = content
        else:
            self.dict['media_id'] = content

    def get_xml(self):
        if self.type == 'text':
            xml_form = """
            <xml>
            <ToUserName><![CDATA[{to_user_name}]]></ToUserName>
            <FromUserName><![CDATA[{from_user_name}]]></FromUserName>
            <CreateTime>{create_time}</CreateTime>
            <MsgType><![CDATA[text]]></MsgType>
            <Content><![CDATA[{content}]]></Content>
            </xml>
            """.format(**self.dict)
        elif self.type == 'image':                                       #More type will be added
            xml_form = """
            <xml>
            <ToUserName><![CDATA[{to_user_name}]]></ToUserName>
            <FromUserName><![CDATA[{from_user_name}]]></FromUserName>
            <CreateTime>{create_time}</CreateTime>
            <MsgType><![CDATA[image]]></MsgType>
            <Image>
            <MediaId><![CDATA[{media_id}]]></MediaId>
            </Image>
            </xml>
            """.format(**self.dict)
        else:
            xml_form=""
            
        return xml_form

    def get_json(self):
        if self.type == 'text':
            json_string = '{"touser":"{to_user_name}","msgtype":"text","text":{"content":"{content}"}}'.format(**self.dict)
        else:
            json_string = '{"touser":"{to_user_name}","msgtype":"image","image":{"media_id":"{media_id}"}}' .format(**self.dict)
        return json_string
