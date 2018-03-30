#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time     : 2018/2/7下午12:28
# @Author   : Saseny Zhou
# @Site     : 
# @File     : json_file.py
# @Software : PyCharm


import json


def write_json_file(obj, path):
    try:
        date = json.dumps(obj, indent=4, ensure_ascii=False)
        f = open(path, 'w', encoding='utf-8')
        f.write(date)
        f.close()
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
