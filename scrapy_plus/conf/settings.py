# encoding: utf-8
#!/usr/bin/env python
"""
@file: settings.py
@author: www.xcooo.cn
@Mail: 602006050@qq.com
"""
from .default_settings import *  # 导入框架中的默认配置

from settings import *  # 由于程序在settings.py的同级目录执行,所以会导入settings中所有配置信息


# 启用的管道类
PIPELINES = [
    'pipelines.BaiduPipeline',
    'pipelines.QiubaiPipeline'
]

# 启用的爬虫类
SPIDERS = [
    'spiders.baidu.BaiduSpider',
    'spiders.qiubai.QiuBaiSpider'
]

# 下载器中间件
DOWNLOADER_MIDDLEWARES = [
    'downloader_middlewares.TestDownloaderMiddleware1'
]

# 爬虫中间件
SPIDER_MIDDLEWARES = [
    'spider_middlewares.TestSpiderMiddleware1'
]