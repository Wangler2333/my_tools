#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 10/28/17 4:03 PM
@author: Saseny Zhou
@File:   shelve_module.py
"""

import shelve
import json

f = shelve.open(r'duanzi')

# print(len(list))
#
# for i in list:
#     f[str(int(len(f.items())) + 1)] = i
#     print(f[str(len(f.items()))])
# # #f['7'] = a
# # # f['shopping'] = {'pig': 'pork', 'cat': 'gas'}
# # #print(f.get('7'))
# #
# f[str(int(len(f.items())) + 1)] = a
#
# print(len(f.items()))
# print(f[str(int(len(f.items())))])

# for i in f.items():
#     print(i)

# f['info'] = {'name': 'saseny', 'password': '123'}
# print(f.get('info'))
# print(f.get('shopping')['cat'])
dict = {}

for i in f.items():
    dict[i[0]] = i[1]
    # print(str(i[1]['content']).replace('\n', ''))

print(dict)
date = json.dumps(dict, ensure_ascii=False)

f = open('duanzi.json', 'w', encoding='utf-8')
f.write(date)
f.close()
