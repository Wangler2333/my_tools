#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from IPy import IP

ip_s = raw_input("请输入IP地址或者网段地址: ")

ips = IP(ip_s)
if len(ips) >1:
    print ('网络地址(net): %s'% ips.net())
    print ('网络掩码地址(netmask): %s'% ips.netmask())
    print ('网络广播地址(broadcast): %s'%ips.broadcast())
    print ('IP地址反向解析(reverse address): %s'%ips.reverseNames()[0])
    print ('网络子网数(subnet): %s'%len(ips))
else:
    print ('IP地址反向解析(reverse address): %s'%ips.reverseNames()[0])

print ('输出十六进制地址(hexadecimal): %s'%ips.strHex())
print ('输出二进制地址(binary ip): %s'%ips.strBin())
print ('输出地址类型(iptype): %s'%ips.iptype())        # PRIVATE / PUBLIC / LOOPBACK
