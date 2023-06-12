# -*- encoding: utf-8 -*-
"""
@File    : wx_handle.py
@Time    : 2023/3/31 2:03 PM
@Author  : nanjiang.xie
@Email   : xie672088678@163.com
@Software: PyCharm
"""
import json

import requests
from flask import request
from loguru import logger

from wx.verification import signature as f_signature  # 签名算法
import wx.receive as receive  # 接收微信消息的地形
import wx.reply as reply  # 将要答复的信息包装成微信需要的xml格式


class WxHandle:

    @staticmethod
    def post():
        """
        响应微信的post请求，微信用户发送的信息会使用Post请求
        :return:
        """
        try:
            # logger.info("接收微信消息->\n" + str(request.data))
            # 对微信传来的xml信息进行解析，解析成我们自定义的对象信息
            receive_msg = receive.parse_xml(request.data)
            json_data = receive_msg.get('content')
            data = {"type": "ios_wx", "name": json_data}
            # 使用json_data请求后台接口
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            response = requests.post(url="https://tool.cupmf.com/hero/detail.php", data=data, headers=headers)
            # 构造回复消息
            if response.status_code ==200:
                return reply.Msg(receive_msg, json.loads(response.text).get('data')).send()
            else:
                logger.error("数据请求失败")
        except Exception:
            logger.error("解析微信XML数据失败!")


        #     # 如果解析成功
        #     if isinstance(receive_msg, receive.Msg):
        #         # 该微信信息为文本信息
        #         if receive_msg.type == "text":
        #             # 创建一条文本信息准备返回给微信，文本内容为“测试成功”
        #             msg = reply.TextMsg(receive_msg, "测试成功")
        #             # 发送我创建的文本信息
        #             return msg.send()
        #         else:
        #             # 该信息不为文本信息时，发送我定义好的一条文本信息给他
        #             return reply.Msg(receive_msg).send()
        # except Exception:
        #     logger.error("解析微信XML数据失败！")
        # return "xml解析出错"

    @staticmethod
    def get():
        """
        响应微信的get请求，微信的验证信息会使用get请求
        这里的验证方式是按照微信公众号文档上的教程来做的
        :return:
        """
        # 微信传来的签名，需要和我生成的签名进行比对
        signature = request.args.get('signature')  # 微信已经加密好的签名，供我比对用
        timestamp = request.args.get('timestamp')  # 这是我需要的加密信息
        nonce = request.args.get('nonce')  # 也是需要的加密信息
        # 判断该请求是否正常，签名是否匹配
        try:
            # 微信传来的签名与我加密的签名进行比对，成功则返回指定数据给微信
            if signature == f_signature(timestamp, nonce):
                # 微信要求比对成功后返回他传来的echost数据给他
                return request.args.get('echostr')
            else:
                return ""
        except Exception:
            logger.error("签名失败！")
        return "签名失败！"
