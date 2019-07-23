# encoding: utf-8
# !/usr/bin/env python
"""
@file: engine.py
@author: www.xcooo.cn
@Mail: 602006050@qq.com
"""
# 引擎对象
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

    def start(self):
        """
        提供启动引擎的入口
        :return:
        """
        self._start_engine()

    def _start_engine(self):
        """
        具体实现引擎的细节
        :return:
        """
        # 1. 调用爬虫的start_request的方法,获取request对象
        start_request = self.spider.start_request()

        # 2. 调用调度器的add_request的方法,添加request对象到调度器中
        self.scheduler.add_request(start_request)

        # 3. 调用调度器的get_request的方法,获取request对象
        request = self.scheduler.get_request()

        # 4. 调用下载器的get_response的方法,获取响应
        response = self.downloader.get_response(request)

        # 5. 调用爬虫的parse的方法,处理响应
        result = self.spider.parse(response)

        # 6. 判断结果的类型,如果是request对象, 重新交给调度器的add_request
        if isinstance(result, Request):
            self.scheduler.add_request(request)
        # 7. 如果不是,交给pipeline的process_item的方法处理结果
        else:

            self.pipline.process_item(result)