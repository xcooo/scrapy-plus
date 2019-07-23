# encoding: utf-8
#!/usr/bin/env python
"""
@file: downloader_middlewares.py.py
@author: www.xcooo.cn
@Mail: 602006050@qq.com
"""
class DownloaderMiddleware(object):
    '''下载器中间件基类'''

    def process_request(self, request):
        '''预处理请求对象'''
        print("这是下载器中间件：process_request方法")
        return request

    def process_response(self, response):
        '''预处理响应对象'''
        print("这是下载器中间件：process_response方法")
        return response