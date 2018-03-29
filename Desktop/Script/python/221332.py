#!/usr/bin/python
# -*- coding: UTF-8 -*-

import re

def Check(pathfile,fromt):
    with open(pathfile) as ae:
        for line in ae:
            if "2017" in line:
                UnitsNumber = line.split()[4]
                if int(fromt) == int(UnitsNumber):
                    if "EVT" in line:
                        print
                        print line.split()[4], line.split()[5]
                        print line
                        print
                        print "----------------------------"


def Check_(pathfile,fromt):
    with open(pathfile) as ae:
        for line in ae:
            if "2017" in line:
                SerialNumber = line.split()[5].split('+')[0]
                if str(fromt) == str(SerialNumber):
                    if "EVT" in line:
                        print
                        print line.split()[4], line.split()[5]
                        print line
                        print
                        print "----------------------------"


while True:
    Fromt = raw_input("Pls input Number:")

    m = re.findall(r"^C",Fromt)
    n = re.findall(r"^[0-9]",Fromt)
    Pathroad ="/Users/saseny/PycharmProjects/Python_Test/Unitsinfo.txt"

    if n:
        Check(Pathroad,Fromt)
    if m:
        Check_(Pathroad,Fromt)




