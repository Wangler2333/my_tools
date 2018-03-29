#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time     : 2017/11/29下午3:55
# @Author   : Saseny Zhou
# @Site     : 
# @File     : folder.py
# @Software : PyCharm Community Edition

import os


def create_folder(path_road):
    if not os.path.isdir(path_road):
        os.makedirs(path_road)


def write_txt(file_, obj):
    f = open(file_, 'a')
    f.write(str(obj) + '\n')
    f.close()


def find_file(path, formet):
    try:
        a = []
        fns = [os.path.join(root, fn) for root, dirs, files in os.walk(path) for fn in files]
        for f in fns:
            if os.path.isfile(f):
                if formet in f:
                    a.append(f)
        return a
    except IOError as o:
        print ('IOError', o)
