#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import dns.resolver


domain = raw_input('请输入域名地址: ')

'''

print "A-->>  www.google.com"
A = dns.resolver.query(domain,'A')

for i in A.response.answer:
    for j in i.items:
        print j.address



print "MX-->>  163.com"
MX = dns.resolver.query(domain,'MX')
for i in MX:
    print 'MX preference =', i.preference, 'mail exchanger =', i.exchange



print "NS-->> baidu.com"
ns = dns.resolver.query(domain,'NS')
for i in ns.response.answer:
    for j in i.items:
        print j.to_text()

'''

print "CNAME-->> "
cname = dns.resolver.query(domain,'CNAME')
for i in cname.response.answer:
    for j in i.items:
        print j.to_text()
