#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     : 2017/10/26上午10:34
# @Author   : Saseny Zhou
# @Site     : 
# @File     : new_one.py
# @Software : PyCharm Community Edition

from collect_log_module import *
import os,sys

t = log_collection('/Users/saseny/Desktop/123/123.log', '/Users/saseny/Desktop/123/321.log')
t.run()


print(os.path.dirname(sys.argv[0]))
t.add_mesaage('你好吗')
