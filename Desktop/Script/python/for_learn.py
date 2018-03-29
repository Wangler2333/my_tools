#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from my_tools import *
from lxml import etree
from bs4 import BeautifulSoup


url = 'http://www.baike.com/wiki/计算机的发展历史'

#print get_crawl(url)

soup1 = BeautifulSoup(get_crawl(url),'lxml')
soup2 = etree.HTML(get_crawl(url))

print type(soup2)
writefile(str(soup1),"/Users/sasenyzhou/Desktop/123.html")

#print soup1.prettify()

tree = soup2.xpath('//p')
tree1 = soup2.xpath('//a')
tree2 = soup2.xpath('//div')


meta = soup2.xpath('//meta')
for i in meta:
    print i.attrib['content']

for i in tree:
    if i.text != None:
        print i.text
        for j in i.attrib:
            print j['alt'].text

for i in tree1:
    if i.text != None:
        print i.text
        print i.attrib

for i in tree2:
    if i.text != None:
        print i.attrib

