#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time     : 2017/12/9上午10:24
# @Author   : Saseny Zhou
# @Site     : 
# @File     : copy_file.py
# @Software : PyCharm Community Edition

import os


def copy_file(path, keys, temp, suffix):
    file_name = [x for x in os.listdir(path) if keys in x and str(x).endswith(str(suffix))]
    target = os.path.join(temp, keys + suffix)
    for i in file_name:
        os.system('mv \'%s\' %s' % (os.path.join(path, i), target))
    if os.path.isfile(target):
        return True
    else:
        return False
