#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time     : 2018/3/6下午6:59
# @Author   : Saseny Zhou
# @Site     : 
# @File     : path.py
# @Software : PyCharm


import sys
from Logs.log import *
from Functions.jsonFile import *
import time
import re
import shutil


def create_folder(path):
    if not os.path.isdir(path):
        os.makedirs(path)


baseDir = os.path.split(os.path.dirname(sys.argv[0]))[0]
resources = os.path.join(baseDir, "Resources")
interval = "<->"

"""Logs文件夹"""
debugLogPath = os.path.join(resources, "Logs")
create_folder(debugLogPath)

"""image文件夹路径"""
imagePath = os.path.join(resources, "image")

"""用户信息路径"""
userInfoJson = os.path.join(resources, "userInfo.json")

"""初始化Log收集类，并开始运行"""
collectLogs = log_collection("/tmp/1_logs.log", os.path.join(debugLogPath, "debug.log"))
collectLogs.run()

"""打印各路径信息"""
collectLogs.logger.info("Resources Path: {}".format(resources))
collectLogs.logger.info("Debug Log Path: {}".format(os.path.join(debugLogPath, "debug.log")))
collectLogs.logger.info("Logs Path: {}".format("/tmp/1_logs.log"))
collectLogs.logger.info("image file Path: {}".format(imagePath))
