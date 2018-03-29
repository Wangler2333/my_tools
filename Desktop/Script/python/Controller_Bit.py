#!/usr/bin/python
# -*- coding: UTF-8 -*-

import plistlib
import re
import pexpect
import os, sys

PlistPath = os.path.dirname(sys.argv[0]) + '/CB_Default.plist'
CB_Log = os.path.dirname(sys.argv[0]) + '/CB_Status.txt'

a = plistlib.readPlist(PlistPath)
b = a['Preburn']
for i in dict.items(b):
    #print i[0], i[1][0], i[1][1]
    c = '(' + i[1][1] + ')'
    with open(CB_Log) as el:
        for line in el:
            if i[1][0] in line and c in line:
                print i[0], i[1][0], i[1][1], line.split('|')[1],line.split('|')[2],line.split('|')[3]
