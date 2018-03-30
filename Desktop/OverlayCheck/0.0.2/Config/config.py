#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time     : 2017/12/9上午8:41
# @Author   : Saseny Zhou
# @Site     : 
# @File     : config.py
# @Software : PyCharm Community Edition

import json
import os
from Config.config_info import *


def write_json_file(obj, path):
    try:
        date = json.dumps(obj)
        f = open(path, 'w')
        f.write(date)
        f.close()
    except IOError as e:
        print('IOError ', e)
        return False


def read_json_file(path):
    try:
        f_obj = open(path, 'r', encoding='utf-8')
        date = json.loads(f_obj.read())
        f_obj.close()
        return date
    except IOError as e:
        print('IOError ', e)
        return False


def write_history(path, string):
    try:
        if not os.path.isfile(path):
            f = open(path, 'a')
            f.write(str(string))
            f.close()
    except TypeError as e:
        pass


def config_check(path):
    if not os.path.isfile(path):
        write_json_file(congfig_info, path)
