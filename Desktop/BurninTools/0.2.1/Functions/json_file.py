#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time     : 2018/3/15上午10:17
# @Author   : Saseny Zhou
# @Site     : 
# @File     : json_file.py
# @Software : PyCharm

import json


def write_json_file(obj, path):
    try:
        date = json.dumps(obj, indent=4)
        f = open(path, 'w')
        f.write(date)
        f.close()
        print("Write json file [%s]" % path)
    except IOError as e:
        return False


def read_json_file(path):
    try:
        f_obj = open(path, 'r', encoding='utf-8')
        date = json.loads(f_obj.read())
        f_obj.close()
        return date
    except IOError as e:
        return False
