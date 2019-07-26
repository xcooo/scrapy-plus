# encoding: utf-8
#!/usr/bin/env python
"""
@file: pipelines.py
@author: www.xcooo.cn
@Mail: 602006050@qq.com
"""
class BaiduPipeline():
    """"
    处理百度的数据的管道
    """
    def process_item(self,item,spider):
        """
        处理item
        :param item:爬虫提取的数据
        :param spider:传递item过来的爬虫
        :return:item
        """
        if spider.name == 'baidu':
            # 对百度的item数据进行处理
            print("百度管道的数据",item.data)
        return item


class QiubaiPipeline():
    """
    处理糗百的数据的管道
    """

    def process_item(self, item, spider):
        """
        处理item
        :param item:爬虫提取的数据
        :param spider:传递item过来的爬虫
        :return:item
        """
        if spider.name == 'qiubai':
            # 对糗百的item数据进行处理
            print("糗百管道的数据", item.data)
        return item