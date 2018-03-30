#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time   : 3/14/18 10:48 PM
# @Author : Saseny.Zhou
# @File   : path.py


import sys
import time
from Logs.log import *
from Functions.json_file import *
from Config.config import *
import re

"""路径定义"""
baseDir = os.path.split(os.path.dirname(sys.argv[0]))[0]
resources = os.path.join(baseDir, "Resources")
debugLogPath = os.path.join(resources, "logs", "debug.log")
imagePath = os.path.join(resources, "images")
configJsonPath = os.path.join(resources, "config.json")
errorJsonPath = os.path.join(resources, "error.json")
unitJsonPath = os.path.join(resources, "units.json")
historyJsonPath = os.path.join(resources, "history.json")  # 记录上次所使用的功能，当再次打开时自动选择上次
errorMessageJsonPath = os.path.join(resources, "errorInfo.json")

"""实例化运行数据收集"""
collectionData = log_collection(log_path="/tmp/logs.log", debug_log=debugLogPath)
collectionData.run()

"""检测配置文件是否存在，不存在则新建默认配置文件"""
if not os.path.isfile(configJsonPath):
    collectionData.logger.info("配置文件不存在,重新生成默认配置文件: {}".format(configJsonPath))
    write_json_file(configInfo, configJsonPath)


def match(rule, text):
    tb = re.compile(rule)
    find = tb.findall(str(text))
    return find
