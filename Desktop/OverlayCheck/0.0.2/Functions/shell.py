#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time     : 2017/12/9上午10:15
# @Author   : Saseny Zhou
# @Site     : 
# @File     : shell.py
# @Software : PyCharm Community Edition


import subprocess
from Functions.copy_file import *


def shell(cmd):
    try:
        run = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        while run.poll() is None:
            print(run.stdout.readline())
        return_code = run.returncode
        return_list = [str(x).replace('\n', '') for x in run.stdout.readlines()]
        return return_code, return_list
    except IOError as e:
        print('IOError', e)


def download_running(args, tmp, product):
    cmd = os.path.join(os.path.dirname(tmp), args['download']['cmd link'])
    code, _ = shell(cmd)
    if code == 0:
        result = copy_file(os.path.join(os.path.expanduser('~'), 'Downloads'), args['download']['file key'], tmp,
                           args['download']['suffix'])
        if result is True:
            return True
        else:
            return False
    else:
        return False
