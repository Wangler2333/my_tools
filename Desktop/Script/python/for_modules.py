#!/usr/bin/python

# -*- coding: UTF-8 -*-


import my_tools
import re


html = my_tools.get_crawl('http://weather.sina.com.cn')
#print html


d = re.findall('<div .*?>(.*?)&#8451;</div>\s*?<p .*?>\s*?(.*?)&nbsp;&nbsp;|&nbsp;&nbsp;(.*?)&nbsp;&nbsp;|&nbsp;&nbsp;(.*?)</p>',html)

for i in d:
    for j in i:
        if re.findall(r'\S*',j):
            print j.replace(' ','').replace('\n','')
