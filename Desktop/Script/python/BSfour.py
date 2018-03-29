#!/usr/bin/env python

import urllib2,urllib,urllib3
from bs4 import BeautifulSoup
from pymongo import MongoClient
from selenium import Webdriver
import pprint

def Download(url, user_agent='wswp', num_retries=2):
    print 'Downloading:', url
    headers = {'User-agent': user_agent}
    request = urllib2.Request(url, headers=headers)
    try:
        html = urllib2.urlopen(url).read().decode('gbk','ascii').encode('utf-8') # ,'ignore'
    except urllib2.URLError as e:
        print 'Download error:', e.reason
        html = None
        if num_retries > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                # recursively retry 5xx HTTP errors
                return Download(url, num_retries-1)

#url = 'http://example.webscraping.com/places/view/United-Kingdom-239'

#html = Download(url)
#print html

#print MongoClient('localhost',27017)

driver = Webdriver.Firefox()
