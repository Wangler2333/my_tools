#!/usr/bin/python

import json
import os
import sys


Path="/Users/sasenyzhou/Desktop/123/C02T8FR6GTFJ_IP.log"
Path1="/Users/sasenyzhou/Desktop/123/C02T8FR6GTFJ.json"

with open(Path) as msg:
    for line in msg:
        if "value" in line or "subsubtestname" in line:
            try:
                print line,
            except TypeError as e:
                print "TypeEror" + e
            with open("/Users/sasenyzhou/Desktop/123d.txt", 'a') as f:
                f.write(str(line))





#with open(Path1) as msg:
#    numbers = json.load(msg)
#    print numbers