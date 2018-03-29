#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time     : 2017/11/29上午8:45
# @Author   : Saseny Zhou
# @Site     : 
# @File     : read_csv.py
# @Software : PyCharm Community Edition

import csv
import os


def read_csv(file_, args):
    fails = []
    if os.path.isfile(file_):
        try:
            f = open(file_, 'r')
            reader = csv.DictReader(f)
            for i in reader:
                fails.append(str(i[args[0]]).replace('/1', '') + ' (Exit code: ' + i[args[1]] + ')')
            f.close()
        except:
            f = open(file_, 'r')
            for i in f:
                a = i.split(',')
                if a[1]:
                    fails.append(str(a[1]).replace('/1', '') + ' (Exit code: ' + a[10] + ')')
            f.close()
    fails = [x for x in set(fails)]
    return fails


args = ['PDCA Key', 'Status Code']
read_csv('/Volumes/DEVELOPMENT/Development/python2/BurninTools/Abnormal/C02VR00AJH97/failures.csv', args)
