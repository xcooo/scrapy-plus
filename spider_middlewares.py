# encoding: utf-8
#!/usr/bin/env python
"""
@file: spider_middlewares.py
@author: www.xcooo.cn
@Mail: 602006050@qq.com
"""
class TestSpiderMiddleware1():
    """
    实现爬虫中间件
    """
    def process_request(self,request):
        """
        处理请求
        :param request:请求对象
        :return:请求对象
        """
        print('TestSpiderMiddleware1 -- process_request')
        return request

    def process_response(self,response):
        """
        处理请求
        :param request:响应对象
        :return:响应对象
        """
        print('TestSpiderMiddleware1 -- process_response')
        return response


class TestSpiderMiddleware2():
    """
    实现爬虫中间件
    """
    def process_request(self,request):
        """
        处理请求
        :param request:请求对象
        :return:请求对象
        """
        print('TestSpiderMiddleware2 -- process_request')
        return request

    def process_response(self,response):
        """
        处理请求
        :param request:响应对象
        :return:响应对象
        """
        print('TestSpiderMiddleware2 -- process_response')
        return response