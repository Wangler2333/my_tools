#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time     : 2017/12/14下午4:45
# @Author   : Saseny Zhou
# @Site     : 
# @File     : coco.py
# @Software : PyCharm Community Edition

import urllib
import urllib2
import lxml.html
import pprint


def parse_form(html):
    tree = lxml.html.fromstring(html)
    data = {}
    for e in tree.cssselect('input'):
        if e.get('name'):
            data[e.get('name')] = e.get('vaule')
    return data


url = 'http://17.239.64.36/pfaportal/pages/create.html'


html = urllib2.urlopen(url).read()
print(html)
form = parse_form(html)
pprint.pprint(form)
