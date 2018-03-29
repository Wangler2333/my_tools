#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 11/6/17 2:04 PM
@author: Saseny Zhou
@File:   ypc2.py
"""

import subprocess
import multiprocessing
import json
import sys
import os


class SMCInfoMonitor(object):
    def __init__(self, ypc2='/usr/local/bin/ypc2'):
        self.ypc2 = ypc2
        self.default = os.path.join(os.path.dirname(sys.argv[0]), 'keysList.json')
        self.checkdefault()

    def shell_command(self, cmd=''):
        shell_cmd = self.ypc2 + cmd
        lines = []
        try:
            shell = subprocess.Popen(shell_cmd, shell=True, stdout=subprocess.PIPE)
            while shell.poll() == None:
                line = str(shell.stdout.readline(), 'utf-8').replace('\n', '')
                if line != '':
                    lines.append(line)
            code = shell.returncode
        except:
            code = 128
        return code, lines

    def keys(self):
        key_list = []
        count = 0
        code, lines = self.shell_command()
        if code == 0:
            for i in lines:
                if count != 0:
                    try:
                        key_list.append(str(i).split()[1])
                    except:
                        pass
                count += 1
        return key_list

    def effectkeys(self):
        final_list = []
        key_list = self.keys()
        for i in key_list:
            end, info = self.shell_command(cmd=' -rdk %s' % i)
            if end == 0:
                final_list.append(i)
        return final_list

    def createjson(self):
        key_dict = {}
        for i in self.effectkeys():
            key_dict[i] = []
        date = json.dumps(key_dict)
        f = open(self.default, 'w')
        f.write(date)
        f.close()

    def checkdefault(self):
        if not os.path.isfile(self.default):
            self.createjson()

    def readdefaultjson(self):
        list_keys = []
        if os.path.isfile(self.default):
            f_obj = open(self.default, 'r', encoding='utf-8')
            date = json.loads(f_obj.read())
            f_obj.close()
            list_keys = date.keys()
        return list_keys


t = SMCInfoMonitor()
list_key = t.readdefaultjson()

result = []


def keyrunning(item):
    a, b = t.shell_command(' -rdk %s' % item)
    red = item, b[0]
    print(red)
    result.append(red)


pool = multiprocessing.Pool(processes=100)
for i in list_key:
    pool.apply_async(keyrunning, (i,))
pool.close()
pool.join()

print(result)
