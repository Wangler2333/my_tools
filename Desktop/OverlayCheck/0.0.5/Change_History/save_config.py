#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time     : 2017/12/15上午8:12
# @Author   : Saseny Zhou
# @Site     : 
# @File     : save_config.py
# @Software : PyCharm Community Edition


from Functions.excel_process import *
from Config.config import *


def excel_report(file):
    product_list = []
    product_dict = {}
    reader = excel_read(file, 1, header=False)
    for i in reader:
        product_tmp = i[0]
        product_list.append(product_tmp)
    for j in product_list:
        product_dict[j] = {
            'line': [],
            'station': []
        }
        for l in reader:
            if j == l[0]:
                product_dict[j]['line'].append(str(l[1]).split('/')[0])
                product_dict[j]['station'].append(str(l[2]).split()[1])
        product_dict[j]['line'] = [x for x in set(product_dict[j]['line'])]
        product_dict[j]['station'] = [x for x in set(product_dict[j]['station'])]
    return product_dict
