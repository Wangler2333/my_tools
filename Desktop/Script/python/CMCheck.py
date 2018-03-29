#!/usr/bin/python
# -*- coding: UTF-8 -*-

import glob
import sys
from plistlib import *

ExpectFile = "/Phoenix/Tools/Settings/CMImageList.plist"
ScanFile = "/Phoenix/Configuration/bundlelist.txt"

def READPlist(path,fromt):
    Plist = readPlist(path)
    a = Plist['CMImage']
    fromt = str(fromt).replace('/','')
    b = []
    with open(ScanFile) as io:
        for line in io:
            if "Bundle_Name_Primary" in line and "694" in line:
                ScanBundle = str(line.split('>')[1].split('<')[0]) + '.dmg'
                b.append(ScanBundle)
    if str(dict.keys(a)) == str(fromt) == str(b):
        print "[PASS] Expected Bundle: " + str(dict.keys(a))
        print "[PASS] Current Bundle: " + str(fromt)
        print "[PASS] Scan Bundle: " + str(b)
        sys.exit(0)
    else:
        print "[FAIL] Expected Bundle: " + str(dict.keys(a))
        print "[FAIL] Current Bundle: " + str(fromt)
        print "[FAIL] Scan Bundle: " + str(b)
        sys.exit(1)

READPlist(ExpectFile,glob.glob("/*.dmg"))

