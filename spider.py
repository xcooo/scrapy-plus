# encoding: utf-8
#!/usr/bin/env python
"""
@file: spider.py
@author: www.xcooo.cn
@Mail: 602006050@qq.com
"""
from scrapy_plus.core.spider import Spider

class BaiduSpider(Spider):
    start_url = ['http://www.douban.com']