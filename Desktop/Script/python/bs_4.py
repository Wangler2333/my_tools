#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 11/6/17 5:53 PM
@author: Saseny Zhou
@File:   bs_4.py
"""

from bs4 import BeautifulSoup
import json

html = BeautifulSoup(open('/private/var/root/Desktop/j79a_keys.html'), "lxml")

#print(html)

a = []
b = []

count = 1
for i in html.find_all('td'):
    ad = str(i.text).split('\n')
    if count <= 5:
        b.append(ad[0])
    if count == 5:
        a.append(b)
        count = 0
        b = []
    count += 1
dict = {}

for p in a[1:]:
    dict[p[0]] = p[1:]


print(dict)

date = json.dumps(dict)
f = open('smcList.json','w')
f.write(date)
f.close()