#!/usr/bin/env python
# -*- coding: UTF-8 -*-


import my_tools
from my_tools import *
from bs4 import BeautifulSoup
import lxml.html
import requests

#url = 'http://weather.sina.com.cn'
url = 'https://kyfw.12306.cn/otn/leftTicket/init'

a = requests.get(url)

print a

#html = get_crawl(url)

#soup = BeautifulSoup(html, 'html.parser')

#print html

'''
tree = lxml.html.fromstring(html)

print tree.text_content
'''

# help(ip_check)
# help(my_tools)
# ip_check("10","172.22.145.137")

# get_weather("/Users/saseny/Desktop/Nvram/123.csv","/Users/saseny/Desktop/Nvram/234.csv")

# for i in  read_csv("/Users/saseny/Documents/Weather/weather_get.csv","normal",""):
#    print i[6]


# a, b = read_csv("/Users/saseny/Documents/Weather/weather_get.csv","Dic","After 24h")
# print a
# for i in b:
#    print i
