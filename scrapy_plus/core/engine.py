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

from .downloader import Downloader
from .pipeline import Pipeline
from .scheduler import Scheduler
from .spider import Spider
from ..http.request import Request

class Engine():
    # 实现对引擎的封装
    def __init__(self,spiders,pipelines=[], spider_mids=[], downloader_mids=[]):
        """
        初始化其他组件
        """
        self.scheduler = Scheduler()
        self.downloader = Downloader()
        self.spiders = spiders  # 字典
        self.pipelines = pipelines
        self.spider_mids = spider_mids  # 列表
        self.downloader_mids = downloader_mids # 列表
        self.total_request_num = 0 # 总的请求数
        self.total_response_num = 0 # 总的响应数

    def start(self):
        """
        提供启动引擎的入口
        :return:
        """
        start_time = datetime.now()
        logger.info('爬虫启动:{}'.format(start_time))
        self._start_engine()
        end_time = datetime.now()
        logger.info('爬虫结束:{}'.format(end_time))
        logger.info('爬虫一共运行:{}秒'.format((end_time-start_time).total_seconds()))
        logger.info('总的请求数量:{}个'.format(self.total_request_num))
        logger.info('总的响应数量:{}个'.format(self.total_response_num))

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

    def _start_engine(self):
        """
        具体实现引擎的细节
        :return:
        """
        self._start_request()  # 初始化请求
        while True:
            self._execute_request_response_item()  # 处理单个请求
            # 循环结束的条件
            if self.total_response_num >= self.total_request_num:
                break
