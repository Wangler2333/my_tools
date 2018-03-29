#!/usr/bin/python

import os
import sys

from subprocess import Popen, PIPE, check_output
from plistlib import readPlistFromString, readPlist

outPutfile = "/Users/sasenyzhou/Desktop/123.csv"
Fail_msg = "FAIL-UPDA"
PassOn_retry="Passed on Retry"
Log_path = "/Users/sasenyzhou/Desktop/processlog.plog"
DefaultFile = "/Users/sasenyzhou/Desktop/Unitsinfo.txt"

os.path.dirname(sys.argv[0])

alfail = []
alfaie = []
lfie = []

def writefile(string):
    with open(outPutfile, 'a') as d:
        d.write(string + '\n')

def systemProfiler(types):
    systemProfilerXml=Popen(["system_profiler", types, "-xml"], stdout=PIPE).communicate()[0]
    pl=readPlistFromString(systemProfilerXml)
    return pl

def SP(types,item_to_check):
    return systemProfiler(types)[0]['_items'][0][item_to_check]

def Check_Fail(file):
    with open(file) as msg:
        for i in msg:
            if Fail_msg in i:
                if PassOn_retry in i:
                    e = i.split('"')[21].replace(',', '')
                else:
                    a = i.split('"')[19]
                    b = i.split('"')[15]
                    c = i.split('"')[21].replace(',', '')
                    d = i.split('"')[-8]
                    tol = a + " #" + b + " " + c + " " + d
                    alfail.append(tol)
    alfaie = set(alfail)
    for i in alfaie:
        if e not in i:
            lfie.append(i)
    return lfie

def Check_unitNumber(file):
    with open(file) as mg:
        for j in mg:
            if SerialNumber in j:
                print j.split()[4]


if not os.path.isfile(outPutfile):
    title = "Unit Number, Serial Number, Config, Location, Error Message, Pass on Retry ?, Remark"
    writefile(title)


SerialNumber = SP("SPHardwareDataType", 'serial_number')
UnitNumber = Check_unitNumber(DefaultFile)

for l in Check_Fail(Log_path):
    print l
    writefile(l)