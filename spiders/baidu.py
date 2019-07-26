# encoding: utf-8
#!/usr/bin/env python
"""
@file: baidu.py
@author: www.xcooo.cn
@Mail: 602006050@qq.com
"""
from scrapy_plus.core.spider import Spider
from scrapy_plus.http.request import Request
from scrapy_plus.item import Item
import urllib.parse

class BaiduSpider(Spider):
    name = 'baidu'
    start_urls = ['http://www.baidu.com']

    def parse(self,response):
        yield Item(response.body[:10])