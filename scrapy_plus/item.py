# encoding: utf-8
# !/usr/bin/env python
"""
@file: item.py
@author: www.xcooo.cn
@Mail: 602006050@qq.com
"""


# item对象

class Item():
    """完成对item对象的封装"""

    def __init__(self, data):
        """
        初始化item
        :param data:数据
        """
        self._data = data

    @property  # 让data属性变成只读
    def data(self):
        return self._data
