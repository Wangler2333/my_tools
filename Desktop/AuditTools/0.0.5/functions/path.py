#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time     : 2018/2/8下午1:19
# @Author   : Saseny Zhou
# @Site     : 
# @File     : path.py
# @Software : PyCharm

import sys
import os
import time
import re
import shutil

"""设置路径信息"""
base_dir = os.path.split(os.path.dirname(sys.argv[0]))[0]
resources = os.path.join(base_dir, "Resources")
images = os.path.join(resources, "images")
command_define_path = os.path.join(resources, "command")
backup_path = os.path.join(resources, "backup")
tmp_path = os.path.join(resources, "temp")
result_path = os.path.join(resources, "result")
# -----------
result_zip_back_up_path = os.path.join(result_path, "zip_back_up")
result_xlsx_back_up_path = os.path.join(result_path, "xlsx_back_up")
# -----------

data_path = os.path.join(resources, "data")
"""显示信息中间间隔"""
interval = "<->"


def create_folder(path):
    """创建文件夹"""
    if not os.path.isdir(path):
        os.makedirs(path)


"""创建文件夹"""
create_folder(tmp_path)
create_folder(result_path)
create_folder(data_path)

"""log 类初始化"""
log_path = os.path.join(resources, "logs")
create_folder(log_path)

from logs.log import *

logFilePath = os.path.join(log_path, "debug.log")
log_collect_append = log_collection(debug_log=logFilePath, log_path="/tmp/log.log")
log_collect_append.run()

log_collect_append.logger.info("<<  ---- * Start Run Application * ----  >>")
