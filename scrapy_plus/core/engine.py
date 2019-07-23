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
    def __init__(self):
        """
        初始化其他组件
        """
        self.spider = Spider()
        self.scheduler = Scheduler()
        self.downloader = Downloader()
        self.pipline = Pipeline()
        self.spider_mid = SpiderMiddleware()
        self.downloader_mid = DownloaderMiddleware()

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

    def _start_engine(self):
        """
        具体实现引擎的细节
        :return:
        """
        # 1. 调用爬虫的start_request的方法,获取request对象
        start_request = self.spider.start_request()

        # 对start_request进行爬虫中间件的处理
        start_request = self.spider_mid.process_request(start_request)

        # 2. 调用调度器的add_request的方法,添加request对象到调度器中
        self.scheduler.add_request(start_request)

        # 3. 调用调度器的get_request的方法,获取request对象
        request = self.scheduler.get_request()

        # request对象经过下载中间件的process_request的方法进行处理
        request = self.downloader_mid.process_request(request)

        # 4. 调用下载器的get_response的方法,获取响应
        response = self.downloader.get_response(request)

        # response对象经过下载中间件的process_response进行处理
        response = self.downloader_mid.process_response(response)

        # response对象经过爬虫中间件的process_response进行处理
        response = self.spider_mid.process_response(response)

        # 5. 调用爬虫的parse的方法,处理响应
        result = self.spider.parse(response)

        # 6. 判断结果的类型,如果是request对象, 重新交给调度器的add_request
        if isinstance(result, Request):
            # 在解析函数得到request对象之后, 使用process_request对request进行处理
            result = self.spider_mid.process_request(result)
            self.scheduler.add_request(result)
        # 7. 如果不是,交给pipeline的process_item的方法处理结果
        else:

            self.pipline.process_item(result)