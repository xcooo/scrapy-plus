# encoding: utf-8
#!/usr/bin/env python
"""
@file: request.py
@author: www.xcooo.cn
@Mail: 602006050@qq.com
"""
# 请求对象


class Request():
    def __init__(self, url, method='GET', headers=None, params=None, data=None):
        """
        完成请求对象的封装
        :param url: 请求的url
        :param method: 请求的方法
        :param headers: 请求头
        :param params: 请求参数
        :param data: 请求体
        """
        self.url = url
        self.method = method
        self.headers = headers
        self.params = params
        self.data = data