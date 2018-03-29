#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from my_tools import *

url = 'http://news.baidu.com'
url2 = "http://news.xinhuanet.com/food/2017-07/27/c_1121386125.htm"
url3 = 'http://blog.csdn.net/zzulp/article/details/6238527'


#print get_crawl(url)
'''
a = re.findall(r'.*?房.*?',get_crawl(url))
b = re.findall(r'<a href="(.*?)">',str(a))

print str(a).decode('string_escape').decode("utf-8")

print get_crawl(b[0])
'''

#print get_crawl(url3)


c = re.findall(r'<p.*?>(.*?)</p>',get_crawl(url3))
for i in c:
    writefile(str(i),'/Users/sasenyzhou/Desktop/Git.txt')


