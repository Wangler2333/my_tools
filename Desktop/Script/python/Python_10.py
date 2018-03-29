#!/usr/bin/python

import os
from shutil import copy
import time
import csv

pathlog = "/Users/saseny/Desktop/__"

Dir = "/Users/saseny/Downloads/Temp"
fb = ".plog"
outputfile = "/Users/saseny/Desktop/python_test.csv"
DefaultFile = "/Users/saseny/Desktop/Desk/Unitsinfo.txt"
Check_Patameter = "FAIL-UPDA"



def display():
    print "---------------------------"
    print "           END             "
    print "---------------------------"

def writefile(string):
    with open(outputfile, 'a') as d:
        d.write(string + '\n')

def Filelist(path,fromt):
    fns = [os.path.join(root, fn) for root, dirs, files in os.walk(path) for fn in files]
    for f in fns:
        if os.path.isfile(f):
            if fromt in f:
                if "PASS" in f or "FAIL" in f:
                    if not os.path.isdir(Dir):
                        os.makedirs(Dir)
                    copy(f,Dir)
                    SerialNumber = os.path.basename(f).split('_')[0]
                    with open(DefaultFile) as msg:
                        for line in msg:
                            if SerialNumber in line:
                                UnitNumber = "#" + line.split()[4]
                    os.system('cd ~/Downloads/Temp ; tar -xzf * &>/dev/null')
                    fnb = [os.path.join(root, fn) for root, dirs, files in os.walk(Dir) for fn in files]
                    for b in fnb:
                        if os.path.isfile(b):
                            if fb in b:
                                with open(b) as log:
                                    for line in log:
                                        if Check_Patameter in line:
                                            a1 = line.split(',')[7].split('"')[1]
                                            a2 = line.split(',')[10].split('"')[1]
                                            a3 = line.split(',')[16].split('"')[1]
                                            a4 = line.split(',')[9].split('"')[1]
                                            a5 = line.split(',')[-4].split('"')[1]
                                            a6 = line.split(',')[12].split('"')[1]
                                            a7 = line.split(',')[21].split('"')[1]
                                            a12 = "#" + a1 + " " + a2
                                            all = UnitNumber + "," + SerialNumber + "," + a7 + "," + a12 + "," + a3 + "," + a4 + "," + a5 + "," + a6
                                            writefile(all)

                    os.system('sleep 3 ; rm -rf ~/Downloads/Temp')


if not os.path.isfile(outputfile):
    title = "Unit Number, Serial Number, Error Code, Test Message, Fail Message, Item, IsPass?, Other Message"
    writefile(title)


#print(len(fns))

Filelist(pathlog,".tgz")



display()
print time.clock()