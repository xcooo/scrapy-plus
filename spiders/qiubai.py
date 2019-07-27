# encoding: utf-8
#!/usr/bin/env python
"""
@file: qiubai.py
@author: www.xcooo.cn
@Mail: 602006050@qq.com
"""
from scrapy_plus.core.spider import Spider
from scrapy_plus.http.request import Request
from scrapy_plus.item import Item
import urllib.parse


# 糗百爬虫
class QiuBaiSpider(Spider):
    name = 'qiubai'
    start_urls = []

    def start_requests(self):
        url_temp = 'https://www.qiushibaike.com/hot/page/{}/'
        for i in range(1,14):
            yield Request(url_temp.format(i))

    def parse(self,response): # 提取页面数据
        # 先分组,再提取
        div_list = response.xpath("//div[@id='content-left']/div")

        for div in div_list[:1]:
            item = {}
            item['name'] = div.xpath(".//h2/text()")[0].strip()
            item['age'] = div.xpath(".//div[contains(@class,'articleGender')]/text()")
            item['age'] = item['age'][0] if len(item['age'])>0 else None
            item['gender'] = div.xpath(".//div[contains(@class,'articleGender')]/@class")
            item['gender'] = item['gender'][0].split(' ')[-1].replace('Icon', '') if len(item['gender'])>0 else None
            item['href'] = urllib.parse.urljoin(response.url, div.xpath("./a/@href")[0])
            # yield Item(item)
            yield Request(
                item['href'],
                parse='parse_detail',
                meta={'item':item}
            )

    def parse_detail(self, response):
        item = response.meta['item']
        item['stats-vote'] = response.xpath("//span[@class='stats-vote']/i/text()")
        item['stats-vote'] = item['stats-vote'][0] if len(item['stats-vote'])>0 else None
        yield Item(item)
