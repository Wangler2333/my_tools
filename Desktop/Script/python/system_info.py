#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time     : 2017/12/4上午10:28
# @Author   : Saseny Zhou
# @Site     : 
# @File     : system_info.py
# @Software : PyCharm Community Edition


from Functions.shell import *
from collections import OrderedDict


class SystemInfo(object):
    def __init__(self, config):
        self.total = config
        self.config = config['system info']

    def hardware(self):
        info_dict = self.config['cmd']
        final = OrderedDict()
        count = 0
        for i in info_dict:
            temp = [key for key in info_dict[i]['read_list'] if info_dict[i]['read_list'][key] is True]
            a, b = shell(i)
            for j in b:
                for n in temp:
                    if n in j:
                        if ':' in j:
                            count += 1
                            final[str(count)] = {n: str(j).split(':')[1].replace(' ', '', 1)}
        return final

    def ssd_info(self):
        ssd_read = self.config['SSD']
        final = OrderedDict()
        if ssd_read['read'] is True:
            a, b = shell(ssd_read['cmd'])
            if a == 0 and len(b) > 0:
                final['SSD'] = b[0]
        return final

    def firmware(self):
        read_cmd = self.config['Firmware']
        final = OrderedDict()
        for i in read_cmd:
            a, b = shell(read_cmd[i])
            if a == 0:
                final[i] = b[0]
        return final

    def combine(self):
        a = self.hardware()
        b = self.ssd_info()
        c = self.firmware()
        for n in [b, c]:
            for i in n:
                count = int(len(a)) + 1
                a[count] = {i: n[i]}
        return a

    def exception_list(self):
        exception = self.total['Exception List']
        return exception
