# encoding: utf-8
# !/usr/bin/env python
"""
@file: response.py
@author: www.xcooo.cn
@Mail: 602006050@qq.com
"""
# 响应对象
from lxml import etree
import json
import re


class Response():
    def __init__(self, url, status_code, headers, body, meta={}):
        """
        完成响应对象的封装
        :param url: 响应url
        :param status_code:响应状态码
        :param headers: 响应头
        :param body: 响应体
        :param meta 接收request meta的值
        """
        self.url = url
        self.status_code = status_code
        self.headers = headers
        self.body = body
        self.meta = meta

    def xpath(self, rule):
        """
        给response对象添加xpath语法, 能够使用xpath提取数据
        :param rule:xpath的字符串
        :return:列表 ,包含element对象或者是字符串
        """
        html = etree.HTML(self.body)
        return html.xpath(rule)

    @property
    def json(self):
        """
        给response对象添加json数据, 能够直接把响应的json数据转化为python类型
        :return:python类型
        """
        return json.loads(self.body.decode())

    def re_findall(self,rule):
        """
        给response对象添加re_findall的方法,能够使用正则从响应中提取数据
        :param rule: 正则表达式字符串
        :return:列表
        """
        return re.findall(rule, self.body.decode())