#!/usr/bin/python

import os
import sys


a = ['you are good man', 'is it olny one', 'one off', 'yes you are right' ]

for i in a:
    if "right" in i:
        b = i.split()[1]
        print b
        a.remove(b)