# encoding: utf-8
#!/usr/bin/env python
"""
@file: pipeline.py
@author: www.xcooo.cn
@Mail: 602006050@qq.com
"""
# 管道对象

class Pipeline():
    # 完成管道对象的封装

    def process_item(self,item):
        """
        实现对item对象进行处理
        :param item:item
        :return:
        """
        print('item:',item.data)