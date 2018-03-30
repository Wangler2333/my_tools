#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time     : 2017/12/9上午8:41
# @Author   : Saseny Zhou
# @Site     : 
# @File     : config.py
# @Software : PyCharm Community Edition

import json


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


congfig_info = {
    "download": {
        "cmd link": "running.sh",
        "file key": "Restore",
        "suffix": ".xls"
    },
    "product_info": {
        "J79A": [
            "F6-1FT-D16",
            "F6-1FT-C16",
            "F6-2FT-F16",
            "F6-2FT-G16"
        ],
        "J80A": [
            "F6-2FT-I16",
            "F6-2FT-H16",
            "F6-2FT-J16"
        ]
    },
    "cycle_setup": {
        "run": True,
        "time": 86400,
        "times": 100
    },
    "user_info": {
        "user name": "",
        "pass word": ""
    },
    "external command": {
        "run": True,
        "command name": "",
        "command path": "",
        "command usage": ""
    },
    "auto_path": ""
}
write_json_file(congfig_info, '/Users/saseny/Desktop/config.json')
