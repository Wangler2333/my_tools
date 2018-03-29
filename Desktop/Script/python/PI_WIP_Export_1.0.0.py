#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# __author__: Saseny Zhou

import re
import csv
import os
import sys
import time

SNList_ = []

message_file = ''


def writefile(string, file):
    try:
        with open(file, 'a') as d:
            d.write(string + '\n')
    except IOError as i:
        print('IOError:', i)


def export_serial_number(file, choose=1):
    with open(file) as f:
        for i in f:
            if choose == 2:
                sn = re.findall(r'C02[A-Z]\w{8}', i)  # 匹配 Serial Number
            if choose == 1:
                sn = re.findall(r'<Primary_UnitID>(C02[A-Z]\w{8}\+\S+)</Primary_UnitID>', i)  # 匹配 WIP (C02[A-Z]\w{8}\+\S+) / (.*?)
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
    choose = 1
    if len(sys.argv) > 1:
        if sys.argv[1] in ['-h', '-H', '--', '-help']:
            print('默认参数使用: 1， 输出 wip. 若输入参数: 2， 则输出 sn.')
            print('1.0.2  修正wip输出不正常.')
            print('Version: 1.0.2 测试版')
            os._exit(1)
        elif sys.argv[1].isalnum():
            if sys.argv[1] == '1':
                choose = 1
            elif sys.argv[1] == '2':
                choose = 2
            else:
                print('数字错误.')
        else:
            print('输入错误.')
            os._exit(1)

    filepath = input("log path: ")

    if " " in filepath:
        print('文件路径存在空格字符,请重新输入.')
        os._exit(1)

    date = time.strftime("%Y_%m_%d_%H_%M_%S")
    if choose == 1:
        Result = os.path.dirname(sys.argv[0]) + '/' + date + '_wip.csv'
    elif choose == 2:
        Result = os.path.dirname(sys.argv[0]) + '/' + date + '_sn.csv'

    cv = set_list(export_serial_number(filepath, choose))

    for i in cv:
        print(i)
        writefile(str(i), Result)

    print("[ WIP 总数量: " + str(len(cv)) + " ]")
