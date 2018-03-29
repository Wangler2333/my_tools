#!/usr/bin/python
# -*- coding: UTF-8 -*-

import commands
import re


a,b = commands.getstatusoutput('diskutil list external')
c = re.findall(r'disk[0-9]',b)
d = set(c)


print a
print b
print c
print d
print len(d)