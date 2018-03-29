#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time     : 2018/3/29下午3:55
# @Author   : Saseny Zhou
# @Site     : 
# @File     : shell.py
# @Software : PyCharm

import subprocess
from Path.path import *


def shell(cmd):
    try:
        run = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        while run.poll() is None:
            if run.stdout.readline():
                collectLogs.logger.info(str(run.stdout.readline(), "utf-8").replace('\n', '').lstrip())
        return_code = run.returncode
        return return_code
    except IOError as e:
        collectLogs.logger.error('IOError', e)
