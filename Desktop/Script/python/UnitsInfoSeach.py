#!/usr/bin/python
# -*- coding: UTF-8 -*-

import re, sys, os

def Check():
    Pathfile = os.path.dirname(sys.argv[0]) + '/Unitsinfo.txt'
    if os.path.isfile(Pathfile):
       Fromat = raw_input("Pls input Message:")
       m = re.findall(r"^C",Fromat)
       n = re.findall(r"^[0-9]",Fromat)
       with open(Pathfile) as ad:
           for line in ad:
               if "2017" in line:
                   if m:
                       SerialNumber = line.split()[5].split('+')[0]
                       if str(Fromat) == str(SerialNumber):
                            if "EVT" in line:
                                print '[ ' + line.split()[4] + ' ' + line.split()[5] + ' ]'
                   if n:
                       UnitsNumber = line.split()[4]
                       if int(Fromat) == int(UnitsNumber):
                            if "EVT" in line:
                                print '[ ' + line.split()[4] + ' ' + line.split()[5] + ' ]'
                   if Fromat == "quit":
                       sys.exit(1)
    else:
        print "Can not find \'Unitsinfo.txt\' file..."
        sys.exit(1)

if __name__ == '__main__':
    while True:
        Check()