#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time     : 2018/2/28下午7:40
# @Author   : Saseny Zhou
# @Site     : 
# @File     : shell.py
# @Software : PyCharm


import subprocess


def shell(cmd):
    try:
        run = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        while run.poll() is None:
            if run.stdout.readline():
                print(str(run.stdout.readline(), "utf-8").replace('\n', '').lstrip())
        return_code = run.returncode
        return return_code
    except IOError as e:
        print('IOError', e)
