#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time     : 2017/12/2下午4:32
# @Author   : Saseny Zhou
# @Site     : 
# @File     : tools.py
# @Software : PyCharm Community Edition


import subprocess
import os
import sys
from shutil import copy

tmp_folder = os.path.join(os.path.dirname(sys.argv[0]), 'temp')


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


def find_path(path):
    a, b = shell('ls %s' % path)
    if a == 0:
        for i in b:
            yield os.path.join(path, i)


def find_file(args):
    for i in args:
        folder_name = os.path.basename(i)
        temp = os.path.join(tmp_folder, folder_name)
        if not os.path.isdir(temp):
            print i
            os.makedirs(temp)
        b = find_path(i)
        for j in b:
            if j.endswith('.txt') or j.endswith('.csv'):
                copy(j, temp)


if len(sys.argv) > 1:
    print " START ".center(20,"*")
    find_file(find_path(sys.argv[1]))
    print " END ".center(20,"*")
