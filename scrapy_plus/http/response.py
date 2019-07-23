# encoding: utf-8
# !/usr/bin/env python
"""
@file: response.py
@author: www.xcooo.cn
@Mail: 602006050@qq.com
"""
# 响应对象


class Response():
    def __init__(self, url, status_code, headers, body):
        """
        完成响应对象的封装
        :param url: 响应url
        :param status_code:响应状态码
        :param headers: 响应头
        :param body: 响应体
        """
        self.url = url
        self.status_code = status_code
        self.headers = headers
        self.body = body
