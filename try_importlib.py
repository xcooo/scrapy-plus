# encoding: utf-8
#!/usr/bin/env python
"""
@file: try_importlib.py
@author: www.xcooo.cn
@Mail: 602006050@qq.com
"""
import importlib

# 启用的管道类
PIPELINES = [
    'pipelines.BaiduPipeline',
    'pipelines.QiubaiPipeline'
]

# 启用的爬虫类
SPIDERS = [
    'spiders.baidu.BaiduSpider',
    'spiders.qiubai. QiuBaiSpider'
]

for pipeline in PIPELINES:
    module_name = pipeline.split('.')[0] # module的名字, 路径
    cls_name = pipeline.split('.')[-1]   # 类名
    module = importlib.import_module(module_name) # 导入module
    cls = getattr(module, cls_name) # 获取module下的类
    print(cls)

for pipeline in SPIDERS:
    module_name = pipeline.rsplit('.')[0] # module的名字, 路径
    cls_name = pipeline.rsplit('.',1)[-1]   # 类名
    module = importlib.import_module(module_name) # 导入module
    cls = getattr(module, cls_name) # 获取module下的类
    print(cls)