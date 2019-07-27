# encoding: utf-8
# !/usr/bin/env python
"""
@file: engine.py
@author: www.xcooo.cn
@Mail: 602006050@qq.com
"""
# 引擎对象
from ..middlewares.spider_middlewares import SpiderMiddleware
from ..middlewares.downloader_middlewares import DownloaderMiddleware
from ..utils.log import logger
from datetime import datetime
from ..conf.settings import ASYNC_TYPE
if ASYNC_TYPE == 'thread':
    from multiprocessing.dummy import Pool
elif ASYNC_TYPE == 'courtine':
    from gevent.pool import Pool
    from gevent.monkey import patch_all
    patch_all()
else:
    raise Exception('不支持的异步方式')

from .downloader import Downloader
from .pipeline import Pipeline
from .scheduler import Scheduler
from .spider import Spider
from ..http.request import Request
from ..conf.settings import PIPELINES, SPIDERS, SPIDER_MIDDLEWARES, DOWNLOADER_MIDDLEWARES, CONCURRENT_REQUEST
import importlib

import time


class Engine():
    # 实现对引擎的封装
    def __init__(self):
        """
        初始化其他组件
        """
        self.scheduler = Scheduler()
        self.downloader = Downloader()
        self.spiders = self._auto_import_instances(SPIDERS, is_spider=True) # 字典
        self.pipelines = self._auto_import_instances(PIPELINES) # 列表
        self.spider_mids = self._auto_import_instances(SPIDER_MIDDLEWARES)  # 列表
        self.downloader_mids = self._auto_import_instances(DOWNLOADER_MIDDLEWARES) # 列表
        self.total_request_num = 0 # 总的请求数
        self.total_response_num = 0 # 总的响应数
        self.pool = Pool(5)   # 实例化线程池对象
        self.is_running = False # 判断程序是否结束的标志

    def _auto_import_instances(self, path ,is_spider=False):
        """
        实现模块的动态导入, 传入模块路径列表, 返回类的实例
        :param path: # 包含模块字符串的列表
        :return: {'name':spider''}/['pipeline等]
        """
        if is_spider:
            instances = {}
        else:
            instances = []

        for p in path:
            module_name = p.rsplit('.',1)[0] # 获取模块的路径名字
            cls_name = p.rsplit('.',1)[-1] # 类名
            module = importlib.import_module(module_name) # 导入模块
            cls = getattr(module, cls_name) # 获取module下的类
            if is_spider:
                instances[cls().name] = cls()
            else:
                instances.append(cls())
        return instances

    def start(self):
        """
        提供启动引擎的入口
        :return:
        """
        start_time = datetime.now()
        logger.info('爬虫启动:{}'.format(start_time))
        logger.info('当前开启的爬虫:{}'.format(SPIDERS))
        logger.info('当前开启的管道:{}'.format(PIPELINES))
        logger.info('当前开启的下载器中间件:{}'.format(DOWNLOADER_MIDDLEWARES))
        logger.info('当前开启的爬虫中间件:{}'.format(SPIDER_MIDDLEWARES))
        self.is_running = True
        self._start_engine()
        end_time = datetime.now()
        logger.info('爬虫结束:{}'.format(end_time))
        logger.info('爬虫一共运行:{}秒'.format((end_time-start_time).total_seconds()))
        logger.info('总的请求数量:{}个'.format(self.total_request_num))
        logger.info('总的响应数量:{}个'.format(self.total_response_num))
        logger.info('总的重复数量:{}个'.format(self.scheduler.repeat_request_nums))

    def _start_request(self):
        """初始化请求,调用爬虫的start_request方法,把所有的请求添加到调度器中"""
        # 1. 调用爬虫的start_request的方法,获取request对象
        for spider_name, spider in self.spiders.items():
            for start_request in spider.start_requests():

                # 对start_request进行爬虫中间件的处理
                for spider_mid in self.spider_mids:
                    start_request = spider_mid.process_request(start_request)

                # 给初始的 请求对象添加spider_name属性
                start_request.spider_name = spider_name

                # 2. 调用调度器的add_request的方法,添加request对象到调度器中
                self.scheduler.add_request(start_request)
                self.total_request_num += 1  # 请求数加1


    def _execute_request_response_item(self):
        """处理单个请求,从调度器取出,发送请求,获取响应,parse函数处理,调度器处理"""
        # 3. 调用调度器的get_request的方法,获取request对象
        request = self.scheduler.get_request()

        if request is None: # 判断request对象是否存在
            return

        # request对象经过下载中间件的process_request的方法进行处理
        for downloader_mid in self.downloader_mids:
            request = downloader_mid.process_request(request)

        # 4. 调用下载器的get_response的方法,获取响应
        response = self.downloader.get_response(request)

        # 把request的meta属性的值传递给response的meta
        response.meta = request.meta

        # response对象经过下载中间件的process_response进行处理
        for downloader_mid in self.downloader_mids:
            response = downloader_mid.process_response(response)

        # response对象经过爬虫中间件的process_response进行处理
        for spider_mid in self.spider_mids:
            response = spider_mid.process_response(response)

        # 根据request 的spider_name的属性 ,获取爬虫实例
        spider = self.spiders[request.spider_name]

        # 获取request对象响应的parse方法
        parse = getattr(spider, request.parse)

        # 5. 调用爬虫的parse的方法,处理响应
        for result in parse(response):

            # 6. 判断结果的类型,如果是request对象, 重新交给调度器的add_request
            if isinstance(result, Request):
                # 在解析函数得到request对象之后, 使用process_request对request进行处理
                for spider_mid in self.spider_mids:
                    result = spider_mid.process_request(result)

                # 对于新的请求,添加spider_name属性
                result.spider_name = request.spider_name

                self.scheduler.add_request(result)
                self.total_request_num += 1  # 请求数加1
            # 7. 如果不是,交给pipeline的process_item的方法处理结果
            else:
                # 遍历所有的管道,对item进行处理
                for pipeline in self.pipelines:
                    result = pipeline.process_item(result,spider)

        self.total_response_num += 1 # 响应数加1

    def _callback(self,temp):
        if self.is_running:
            self.pool.apply_async(self._execute_request_response_item, callback=self._callback)

    def _start_engine(self):
        """
        具体实现引擎的细节
        :return:
        """
        self.pool.apply_async(self._start_request)  # 初始化请求
        for i in range(CONCURRENT_REQUEST):
            self.pool.apply_async(self._execute_request_response_item, callback=self._callback)
        while True:
            time.sleep(0.0001) # 避免cpu空转,影响性能
            # self._execute_request_response_item()  # 处理单个请求
            # 循环结束的条件
            # 总的响应数量 + 总的重复数量 == 总的请求数量
            if self.total_request_num !=0: # 不让主线程太快的结束
                if self.total_response_num + self.scheduler.repeat_request_nums >= self.total_request_num:
                    self.is_running = False
                    break
