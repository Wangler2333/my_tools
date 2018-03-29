#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 10/28/17 3:12 PM
@author: Saseny Zhou
@File:   json_module.py
"""

import json


def _write_json_file(obj, path):
    try:
        date = json.dumps(obj)
        f = open(path, 'w')
        f.write(date)
        f.close()
    except IOError as e:
        print('IOError ', e)


def _read_json_file(path):
    try:
        f_obj = open(path, 'r', encoding='utf-8')
        date = json.loads(f_obj.read())
        f_obj.close()
        return date
    except IOError as e:
        print('IOError ', e)


if __name__ == '__main__':
    pass