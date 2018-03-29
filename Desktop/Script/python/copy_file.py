#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time     : 2017/11/29下午4:34
# @Author   : Saseny Zhou
# @Site     : 
# @File     : copy_file.py
# @Software : PyCharm Community Edition


from shutil import copy


def copy_file(source, target):
    try:
        copy(source, target)
    except IOError as e:
        print '[FAIL] copy file fail.'
