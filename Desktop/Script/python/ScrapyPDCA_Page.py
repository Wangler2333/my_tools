#!/usr/bin/env python
# -*- coding: UTF-8

import urllib
import urllib2

f_path = "/Users/saseny/Desktop/crawl_page.html"

#with open(f_path) as f_obj:
#    print f_obj


last_crawl = urllib2.urlopen(f_path, timeout=30).read()

print last_crawl