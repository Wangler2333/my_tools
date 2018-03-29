#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import psutil
import datetime
from subprocess import Popen, PIPE
import IPy

ip = IPy.IP('172.22.145.30')

print ip.reverseNames()
print ip.iptype()           # PRIVATE 私网类型

print IPy.IP('8.8.8.8').iptype()     # PUBLIC 公网类型

print ip.int()            # 转换成整型格式
print ip.strHex()         # 转换成十六进制格式
print ip.strBin()         # 转换成二进制格式


print (IPy.IP(0xac16911e))   # 十六进制转成IP格式

print (IPy.IP('192.168.1.0').make_net('255.255.255.0'))   # 根据IP与掩码生产网段格式
print (IPy.IP('192.168.1.0/255.255.255.0',make_net=True))
print (IPy.IP('192.168.1.0-192.168.1.255',make_net=True))

#print IPy.IP('192.168.1.0/24').strNormal(0)

a = [0,1,2,3,4,5]
for i in a:
    print IPy.IP('192.168.1.0/24').strNormal(i)

'''
判断两个网段是否存在重叠，采用IPy提供的overlaps方法
'''

print IPy.IP('192.168.0.0/23').overlaps('192.168.1.0/24')

print IPy.IP('192.168.1.0/24').overlaps('192.168.2.0')

