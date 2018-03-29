#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import urllib2
import re
import urllib
import os
import time
import urllib3
import pprint
import cookielib
import mechanize
import lxml.html
from BeautifulSoup import BeautifulSoup
import plistlib

URL = "http://17.239.64.36/cgi-bin/WebObjects/QCR.woa/wa/logon"
PDCAIPAdress = '17.239.64.36'


def Download(url, user_agent='wswp', num_retries=2):
    print 'Downloading:', url
    headers = {'User-agent': user_agent}
    request = urllib2.Request(url, headers=headers)
    try:
        html = urllib2.urlopen(url).read()  # .decode('gbk','ascii').encode('utf-8') # ,'ignore'
    except urllib2.URLError as e:
        print 'Download error:', e.reason
        html = None
        if num_retries > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                # recursively retry 5xx HTTP errors
                return Download(url, num_retries - 1)
    return html


def parse_form(html):
    tree = lxml.html.fromstring(html)
    data = {}
    for e in tree.cssselect('form input'):
        if e.get('name'):
            data[e.get('name')] = e.get('value')
    return data


def crawl_sitemap(url):
    postdata = urllib.urlencode({
        'UserName': "Danny.Liu",
        'Password': "apple1234567890"
    })
    #
    req = urllib2.Request(
        url=url,
        data=postdata
    )
    result = urllib2.urlopen(req).read()
    linst = re.search('<a href="(.*?)">\s*?<div id = "systems_yield">Systems Yield</div>', result)
    # linst = re.search('</div>\s*?<a href="(.*?)">',result)
    # print linst
    tep = linst.group(1)

    # match = re.search('<a href="(.*?)">\s*?<span id = "product_history">Product History</span>', result)
    # tmp = match.group(1)
    # print tep
    # print tmp
    UNITURL = 'http://%s%s' % (PDCAIPAdress, tep)
    result_ = urllib2.urlopen(UNITURL, timeout=30).read()
    # print result_
    # print result_
    asd = re.search(r'<form name="criteria" method="post" action="(.*?)">&nbsp;<table border = "0">', result_)
    UNITURL1 = 'http://%s%s' % (PDCAIPAdress, asd.group(1))
    # UNITURL1 = "http://17.239.64.36/cgi-bin/WebObjects/QCR.woa/9/wo/ztzYPDUJUmCRoyb9HOSt4w/459.5.1.1"
    print UNITURL1

    Date1 = "06/05/2017"
    Date2 = "06/06/2017"
    MyTime1 = "00:59:00"
    MyTime2 = "10:59:00"

    postdata = urllib.urlencode({
        'startDateField': Date1,
        'endDateField': Date2,
        '5.1.1.3.5.1': MyTime1,
        '5.1.1.3.7.3.1': MyTime2,
        '5.1.1.5': 'Find Data',
    })

    req1 = urllib2.Request(
        url=UNITURL1,
        data=postdata
    )

    result1 = urllib2.urlopen(req1).read()
    ssdhd = parse_form(result1)
    pprint.pprint(ssdhd)


    UNITURL2_ = re.search('<form name="criteria" method="post" action="(.*?)">', result1)
    UNITURL2 = 'http://%s%s' % (PDCAIPAdress, UNITURL2_.group(1))

    print UNITURL2

    postdata = urllib.urlencode({
        # '5.1.1.11.21.5.1': "false",
        'startDateField': Date1,
        'endDateField': Date2,
        '5.1.1.3.5.1': MyTime1,
        '5.1.1.3.7.3.1': MyTime2,
        '5.1.1.11.21.5.1': '5.1.1.11.21.5.0',
        '5.1.1.11.21.7.1.44.1': '5.1.1.11.21.7.1.44.1',
        '5.1.1.11.21.7.1.45.1': '5.1.1.11.21.7.1.45.1',
        '5.1.1.11.21.7.1.50.1': '5.1.1.11.21.7.1.50.1',
        '5.1.1.11.21.7.1.51.1': '5.1.1.11.21.7.1.51.1',
        '5.1.1.11.23.0': "14",
        '5.1.1.15.1.0': 'Calc Yields',
    })

    req2 = urllib2.Request(
        url=UNITURL2,
        data=postdata
    )

    # result2 = urllib2.urlopen(req2).read()


crawl_sitemap(URL)
