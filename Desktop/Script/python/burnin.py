#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time     : 2017/11/17下午3:37
# @Author   : Saseny Zhou
# @Site     : 
# @File     : burnin.py
# @Software : PyCharm Community Edition


import csv
import json

# print dir(csv)

a = '/Users/saseny/Desktop/J132/_tools/summary.csv'

f = open(a, 'r')
d = csv.DictReader(f)
# e = csv.reader(f)
# f.close()

count = 0
for i in d:
    if count < 5:
        print i['# Test Action Result']
    count += 1

# for i in e:l
#     print i


f.close()
