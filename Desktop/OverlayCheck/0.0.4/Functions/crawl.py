#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time     : 2017/12/14下午1:54
# @Author   : Saseny Zhou
# @Site     : 
# @File     : crawl.py
# @Software : PyCharm Community Edition


import urllib.request
import shutil
import ssl

content = ssl._create_unverified_context()
url = 'https://172.24.70.50/groundhog/tools/restore_report.php?download=1'


def crawl(path):
    try:
        r = urllib.request.urlopen(urllib.request.Request(url), context=content)
        with open(path + '/' + 'Restore.xls', 'wb') as f:
            shutil.copyfileobj(r, f)
        return True
    except:
        return False
