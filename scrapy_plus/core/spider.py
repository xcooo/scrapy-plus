# encoding: utf-8
# !/usr/bin/env python
"""
@file: spider.py
@author: www.xcooo.cn
@Mail: 602006050@qq.com
"""
# 爬虫组件的封装
from ..http.request import Request
from ..item import Item


class Spider():
    start_url = 'https://www.baidu.com'  # 爬虫最开启请求的url

    def start_request(self):
        """
        构造start_url地址的请求
        :return: request对象
        """
        return Request(self.start_url)

    def parse(self, response):
        """
        默认处理start_url地址对应的响应
        :return: item 或者 request
        """
        return Item(response.body)
