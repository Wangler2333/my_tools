#!/usr/bin/env python
# -*- coding: UTF-8 -*-


import my_tools
from my_tools import *
from bs4 import BeautifulSoup
from lxml import etree


link = "/Users/saseny/Desktop/gethtml.html"

soup = BeautifulSoup(open(link),'html.parser')
print soup.prettify()