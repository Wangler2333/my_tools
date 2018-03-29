#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time     : 2017/11/29上午11:12
# @Author   : Saseny Zhou
# @Site     : 
# @File     : hashTool.py
# @Software : PyCharm Community Edition


import hashlib
import sys

password = 'sasenyzhou'


def hash_():
    a = hashlib.sha256()
    a.update(password)
    return a.hexdigest()


def hash_check(string):
    if string != hash_():
        print 'CheckSum Not Mactch, Pls check.'
        sys.exit(1)
