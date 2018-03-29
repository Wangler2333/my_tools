#!/usr/bin/python

import sys

File = sys.argv[1]

for i in open(File):
    if 'QSMC' in i:
        print i