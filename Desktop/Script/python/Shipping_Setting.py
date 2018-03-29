#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time     : 2017/11/28下午4:31
# @Author   : Saseny Zhou
# @Site     : 
# @File     : Shipping_Setting.py
# @Software : PyCharm Community Edition

from xml.dom.minidom import parse
import xml.dom.minidom

name = '/Users/saseny/Desktop/J132/shipping-setting/11_21/Kestrel/Tables/Kestrel.ktproj/tables/SS-Kestrel.xml'

# DOMTree = xml.dom.minidom.parse(name)
# collection = DOMTree.documentElement
#
# title_list = ['metadata', 'functionId', 'interactive', 'functionGroup', 'functionName', 'functionCategory']
#
# t = collection.getElementsByTagName("Kstl_TestFunctionDescriptor")
#
# for i in t:
#     for j in title_list:
#         try:
#             a = i.getElementsByTagName(j)[0]
#             print a.childNodes[0].data
#         except:
#             print None

from xml.etree.ElementTree import ElementTree

doc = ElementTree(file=name)
# ingredients = doc.find('memberStatements')
# print ingredients
