#!/usr/bin/python
# _*_ coding:utf8 _*_

import urllib2,cookielib
import requests
import pickle
import PIL,io
import BeautifulSoup
import lxml.html
import re
import tkColorChooser
import tkMessageBox

#url = 'https://www.qt.io/download-open-source/?hsCtaTracking=f977210e-de67-475f-a32b-65cec207fd03%7Cd62710cd-e1db-46aa-8d4d-2f1c1ffdacea#section-2'
#url = 'https://www.baidu.com'
#url = 'file:///Users/sasenyzhou/Desktop/NewResult1.html'

#Html = urllib2.urlopen(url).read()
#result = BeautifulSoup.BeautifulSoup(url,'html.parser')
#result = lxml.html.fromstring(Html)
#BeautifulSoup..
#td = result.cssselect('tr#places_area_row > td.w2p_fw')
#ab = td.text_content()

#print ab
#urllib2.Request

#r = re.findall(r'<td align = "CENTER">(.*?)</td>',Html)

#print r

with open('/Users/sasenyzhou/Desktop/NewResult1.txt') as f:
    for line in f:
       if "<" not in line and "}" not in line and "{" not in line:
           if len(line.split()) == 1:
               print line.split()