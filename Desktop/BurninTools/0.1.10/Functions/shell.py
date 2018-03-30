#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time     : 2018/3/15下午3:35
# @Author   : Saseny Zhou
# @Site     : 
# @File     : shell.py
# @Software : PyCharm


import subprocess


def shell(cmd, times=3):
    try:
        run = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        while run.poll() is None:
            pass
        return_code = run.returncode
        return_list = [str(x, "utf-8").replace("\n", "") for x in run.stdout.readlines()]
        return return_code, return_list
    except:
        times -= 1
        if times > 0:
            shell(cmd, times=times)
