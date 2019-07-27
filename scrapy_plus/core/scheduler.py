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
import w3lib.url
from hashlib import sha1
import six
from ..utils.log import logger
from ..utils.queue import Queue as RedisQueue
from ..conf.settings import SCHEDULER_PERSIST
from ..utils.set import NoramlFilterContainer, RedisFilterContainer


def _to_bytes(string):
    if six.PY2:  # 当环境为python2
        if isinstance(string, str):
            return string
        else:
            return string.encode('utf-8') # unicode类型转化为字节类型
    elif six.PY3: # 当环境为python3
        if isinstance(string, str):
            return string.encode('utf-8')
        else:
            return string


class Scheduler():
    def __init__(self):
        if not SCHEDULER_PERSIST:
            self.queue = Queue()   # 存储的是待抓取的请求
            # 不使用分布式的时候,使用python的集合存储指纹
            self._filter_container = NoramlFilterContainer()
        else:
            # 当使用分布式的时候,使用redis队列
            self.queue = RedisQueue()
            # 使用分布式的时候,使用redis的集合存储指纹
            self._filter_container = RedisFilterContainer()

        # self._filter_container = set() # 保存指纹的集合

        self.repeat_request_nums = 0 # 统计请求重复的数量

    def add_request(self, request):
        """
        添加请求对象
        :param request:
        :return:None
        """
        if self._filter_request(request):
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
        实现对请求对象的去重
        :return:bool
        """
        # 给request对象添加一个fp属性, 保存指纹
        request.fp = self._gen_fp(request)
        if not  self._filter_container.exists(request.fp): # 判断指纹不在指纹集合中
            # 把指纹添加到指纹集合中
            self._filter_container.add_fp(request.fp)
            return True
        else:
            logger.info('发现重复的请求:<{} {}>'.format(request.method,request.url))
            self.repeat_request_nums += 1


    def _gen_fp(self, request):
        """
        生成请求对象的指纹
        :param request:
        :return: 指纹的字符串
        """
        # 对url, 请求体, 请求参数, 请求方法进行加密,得到指纹
        # 对url地址进行排序
        url = w3lib.url.canonicalize_url(request.url)

        # 请求方法
        method = request.method.upper()

        # 请求参数
        params = request.params if request.params is not None else {}
        params = str(sorted(params.items(),key=lambda x:x[0]))

        # 请求体排序
        data = request.data if request.data is not None else {}
        data = str(sorted(data.items(),key=lambda x:x[0]))

        # 使用sha1 对数据进行加密
        fp = sha1()
        # 添加url地址
        fp.update(_to_bytes(url))
        # 添加请求方法
        fp.update(_to_bytes(method))
        # 添加请求参数
        fp.update(_to_bytes(params))
        # 添加请求体
        fp.update(_to_bytes(data))

        return fp.hexdigest() # 返回16进制的字符串