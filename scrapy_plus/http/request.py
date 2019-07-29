# encoding: utf-8
#!/usr/bin/env python
"""
@file: request.py
@author: www.xcooo.cn
@Mail: 602006050@qq.com
"""
# 请求对象


class Request():
    def __init__(self, url, method='GET', headers=None, params=None, data=None, parse='parse', meta=None,filter=True):
        """
        完成请求对象的封装
        :param url: 请求的url
        :param method: 请求的方法
        :param headers: 请求头
        :param params: 请求参数
        :param data: 请求体
        :param parse 请求对象响应的处理函数的函数名
        :param meta 在不同的解析函数传递数据
        """
        self.url = url
        self.method = method
        self.headers = headers
        self.params = params
        self.data = data
        self.parse = parse
        self.meta = meta
        self.filter = filter # 默认会进行请求的去重,如果为False,不进行去重