#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time     : 2017/11/29上午8:53
# @Author   : Saseny Zhou
# @Site     : 
# @File     : shell.py
# @Software : PyCharm Community Edition

import subprocess


def shell(cmd):
    try:
        run = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        while run.poll() is None:
            pass
        return_code = run.returncode
        return_list = [str(x).replace('\n', '') for x in run.stdout.readlines()]
        return return_code, return_list
    except IOError as e:
        print('IOError', e)
