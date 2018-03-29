#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import re
import commands
import time
import csv
import os
from my_tools import writefile

def ip_check(cycle_time_set):
    '''
    :param cycle_time_set:        提供每次循环的时间间隔
    :return:                      生成的结果存储在当前用户目录下
    '''
    count = 0
    file_path = os.path.expanduser('~') + '/ip_list.csv'

    while True:

        if not os.path.isfile(file_path):
            a = "Update Time," + "Ip list"
            writefile(str(a), file_path)

        if count == int(cycle_time_set):
            count = 0

        if count == 0:
            cmd = "ifconfig"
            date = time.strftime("%Y/%m/%d %H:%M:%S")
            write_list = []
            write_list.append(str(date))

            try:
                ifconfig = commands.getoutput(cmd)
                ip_info = re.findall(r'[0-9]*\.[0-9]*\.[0-9]*\.[0-9]*',ifconfig)

                r = write_list + ip_info
                writer = csv.writer(open(file_path, 'a'))
                writer.writerow(r)

            except:
                pass

        count = count + 1
        time.sleep(1)


ip_check("2")