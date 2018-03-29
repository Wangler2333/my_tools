#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import builtwith
import whois
import urllib2
import re
import itertools
import chardet
import Dialog,DjangoCaptcha
import Django

url = "http://example.webscraping.com"


def Download(url, user_agent='wswp', num_retries=2):
    print 'Downloading:', url
    headers = {'User-agent': user_agent}
    request = urllib2.Request(url, headers=headers)
    try:
        html = urllib2.urlopen(url).read().decode('gbk', 'ascii').encode('utf-8')  # ,'ignore'
    except urllib2.URLError as e:
        print 'Download error:', e.reason
        html = None
        if num_retries > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                # recursively retry 5xx HTTP errors
                return Download(url, num_retries - 1)
    return html

def crawl_sitemap(url):
    links = []
    # download the sitemap file
    sitemap = Download(url)
    print sitemap
    print chardet.detect(sitemap)['encoding']
    # extracy the sitemap links
    # links_ = re.findall(r'href="http:.*?"',sitemap)
    links = re.findall('<loc>(.*?)</loc>', sitemap)
    # for i in links_:
    #    links.append(str(i).split('\"')[1])
    print links
    print len(links)
    # download each link
    if __name__ == '__main__':
        if __name__ == '__main__':
            for link in links:
                html = Download(link)
                print html
                # scrape html here
                # ...


# print builtwith.parse(url)
# print whois.whois(url)
# print Download(url)
crawl_sitemap(url)
