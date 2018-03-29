#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time     : 2017/11/27下午7:31
# @Author   : Saseny Zhou
# @Site     : 
# @File     : testd.py
# @Software : PyCharm Community Edition

import re

f = open('/Users/saseny/Desktop/testd.log', 'r')
f_obj = f.readlines()
f.close()

Diag_test = {
    "componentIdentifier": "",
    "component": "",
    "id": "",
    "test": '',
    "specifications": {}
}

keys = ['[ERROR]', '[DEBUG]', '[INFO]', '\"test\"']
list_ = []

for i in f_obj:
    a = re.findall(r'\"id\" : \"(.*?)\"', i)
    if len(a) > 0:
        list_.append(a[0])
    for j in keys:
        if j in i:
            print i.replace('\n', '')

list_ = [x for x in set(list_)]

print list_
