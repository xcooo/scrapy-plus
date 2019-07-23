# encoding: utf-8
# !/usr/bin/env python
"""
@file: downloader.py
@author: www.xcooo.cn
@Mail: 602006050@qq.com
"""
# 下载器
import requests
from ..http.response import Response


class Downloader():
    # 完成对下载器的封装
    def get_response(self, request):
        """
        实现构造请求对象,发送请求,返回响应
        :param request: request
        :return: response
        """
        if request.method.upper() == 'GET':
            resp = requests.get(request.url, headers=request.headers, params=request.params)
        elif request.method.upper() == 'POST':
            resp = requests.post(request.url, headers=request.headers, params=request.params, data=request.data)
        else:
            raise Exception('请求方法不支持: <{}>'.format(request.method))

        return Response(url=resp.url, headers=resp.headers, body=resp.content, status_code=resp.status_code)
