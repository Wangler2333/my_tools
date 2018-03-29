#!/usr/bin/python
# -*- coding: UTF-8 -*-

import time, datetime
import sys
import os
from shutil import copy,rmtree


class copyProcesslog(object):

    def __init__(self):
        self.Paratmater = raw_input("Pls input txt file for SN log collect:\n")
        self.source = raw_input("Pls input Log Disk:\n")
        self.target = os.path.dirname(sys.argv[0]) + "/LOG"

    def findout(self):
        try:
            with open(self.Paratmater) as fe:
                for line in fe:
                    self.LiteSN = str(line)
                    fns = [os.path.join(root, fn) for root, dirs, files in os.walk(self.source) for fn in files]
                    for f in fns:
                        if os.path.isfile(f):
                            if self.LiteSN in f:
                                copy(f,self.target)
        except IOError as i:
            print ('IOError',i)

if __name__ == '__main__':
    copyProcesslog().findout()