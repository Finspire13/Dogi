from xml.etree import ElementTree


class ReceiveMessage:
    def __init__(self, web_data):
        xml_data = ElementTree.fromstring(web_data)
        self.to_user_name = xml_data.find('ToUserName').text
        self.from_user_name = xml_data.find('FromUserName').text
        self.create_time = xml_data.find('CreateTime').text
        self.message_type = xml_data.find('MsgType').text
        self.message_id = xml_data.find('MsgId').text
        if self.message_type == 'text':
            self.content = xml_data.find('Content').text.encode("utf-8")
        elif self.message_type == 'image':
            self.picture_url = xml_data.find('PicUrl').text
            self.media_id = xml_data.find('MediaId').text
