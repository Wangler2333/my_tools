#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import re
import csv
import os
import sys

SNList_ = []


def writefile(string, file):
    try:
        with open(file, 'a') as d:
            d.write(string + '\n')
    except IOError as i:
        print ('IOError:', i)


def export_serial_number(file):
    with open(file) as f:
        for i in f:
            # sn = re.findall(r'C02[A-Z]\w{8}', i)   # 匹配 Serial Number
            sn = re.findall(r'<Primary_UnitID>(.*?)</Primary_UnitID>', i)  # 匹配 WIP
            if len(sn) > 0:
                for j in sn:
                    SNList_.append(j)
    return SNList_


def set_list(list):
    d = []
    a = set(list)
    for i in a:
        d.append(i)
    return d


if __name__ == '__main__':
    filepath = raw_input("log path: ")
    Result = os.path.dirname(sys.argv[0]) + '/snlist.csv'
    cv = set_list(export_serial_number(filepath))

    print
    print "[ WIP 总数量: " + str(len(cv)) + " ]"
    print

    #for i in cv:
    #    print i
    #    writefile(str(i), Result)
