# encoding: utf-8
#!/usr/bin/env python
"""
@file: default_settings.py
@author: www.xcooo.cn
@Mail: 602006050@qq.com
"""
import logging

# log默认的配置
DEFAULT_LOG_LEVEL = logging.INFO    # 默认等级
DEFAULT_LOG_FMT = '%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s: %(message)s'   # 默认日志格式
DEFUALT_LOG_DATEFMT = '%Y-%m-%d %H:%M:%S'  # 默认时间格式
DEFAULT_LOG_FILENAME = 'log.log'    # 默认日志文件名称

# 设置并发的数量
CONCURRENT_REQUEST = 5

# 选择线程池的方式
ASYNC_TYPE = 'courtine' #thread