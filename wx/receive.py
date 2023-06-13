# -*- encoding: utf-8 -*-
"""
@File    : receive.py
@Time    : 2023/3/31 2:04 PM
@Author  : nanjiang.xie
@Email   : xie672088678@163.com
@Software: PyCharm
"""
import json
import xml.etree.ElementTree as ET


def parse_xml(web_data):
    """
    解析微信传递来的消息，根据消息类型转换为不同的对象
    :param web_data:
    :return:
    """
    # 解析xml数据
    xml = ET.fromstring(web_data)
    content = xml.find('Content').text
    content = content.replace('\\\\xb5', '\\xb5')
    content = content.replace('\\\\x', '\\x')
    # decoded_content = content.encode('latin1').decode('unicode_escape').encode('latin1').decode('utf-8')
    decoded_content = content.decode('utf-8')
    msg = {}
    msg['touser'] = xml.find('ToUserName').text
    msg['fromuser'] = xml.find('FromUserName').text
    msg['create_time'] = xml.find('CreateTime').text
    msg['msgtype'] = xml.find('MsgType').text
    msg['content'] = decoded_content
    msg['msgid'] = xml.find('MsgId').text

    return msg


class Msg:
    """
    定义消息的基本格式，是一些类型消息的父类，解析XML格式的微信信息
    """

    def __init__(self, xml):
        self.toUser = xml.find('ToUserName').text  # 公众号的微信号
        self.fromUser = xml.find('FromUserName').text  # 发送消息的用户的openid
        self.time = xml.find('CreateTime').text  # 创建时间
        self.type = xml.find('MsgType').text  # 消息类型
        self.id = xml.find('MsgId').text  # 该消息的id，每天消息都有独立的id


    def to_json(self):
        return json.dumps({
            'toUser': self.toUser,
            'fromUser': self.fromUser,
            'time': self.time,
            'type': self.type,
            'id': self.id
        })


class TextMsg(Msg):
    """
    解析文字类信息
    """

    def __init__(self, xml):
        Msg.__init__(self, xml)  # 为父类的属性赋值
        self.content = xml.find('Content').text.encode("utf-8")  # 传递来的信息需要经过utf-8编码

    def to_json(self):
        json_data = super().to_json()
        json_data['name'] = self.content
        return json_data


class ImageMsg(Msg):
    """
    解析图片信息
    """

    def __init__(self, xml):
        Msg.__init__(self, xml)
        self.picUrl = xml.find('PicUrl').text
        self.mediaId = xml.find('MediaId').text

    def to_json(self):
        json_data = super().to_json()
        json_data['picUrl'] = self.picUrl
        json_data['mediaId'] = self.mediaId
        return json_data
