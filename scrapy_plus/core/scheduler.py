# encoding: utf-8
#!/usr/bin/env python
"""
@file: scheduler.py
@author: www.xcooo.cn
@Mail: 602006050@qq.com
"""
"""
调度器模块的封装
"""
# six第三方库,适配python2 和 python3
from six.moves.queue import Queue


class Scheduler():
    def __init__(self):
        self.queue = Queue()

    def add_request(self, request):
        """
        添加请求对象
        :param request:
        :return:None
        """
        # self._filter_request(request)
        self.queue.put(request)

    def get_request(self):
        """
        获取一个请求对象并返回
        :return:request
        """
        try:
            request = self.queue.get(block=False)
            return request
        except:
            return None

    def _filter_request(self,request):
        """
        去重,暂时不实现
        :return:bool
        """
        pass