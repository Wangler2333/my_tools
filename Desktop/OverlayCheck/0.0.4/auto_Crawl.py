#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time     : 2017/12/14下午1:43
# @Author   : Saseny Zhou
# @Site     : 
# @File     : auto_Crawl.py
# @Software : PyCharm Community Edition


import urllib.request
import shutil
import ssl

url = 'https://172.24.70.50/groundhog/tools/restore_report.php?download=1'
log_folder = '/Users/saseny/Desktop/Run_in'
content = ssl._create_unverified_context()

r = urllib.request.urlopen(urllib.request.Request(url), context=content)

with open(log_folder + '/' + '123.xls', 'wb') as f:
    shutil.copyfileobj(r, f)
