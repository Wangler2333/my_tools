#!/usr/bin/python
# For Run-in Log Process
# Created by Saseny on 2017/03/04
# Version 1.2
# Base on 1.1 / Add Special Error Check (Device not found & Core.Check.Config & Core.Check.ModelFirmware)
# 'Unitsinfo.txt' is test unit info, if not exist then no UnitNumber&Config outPut

import os
import sys
from subprocess import Popen, PIPE
from plistlib import readPlistFromString

Set_1 = []
Set_2 = []
Set_3 = []

Location = "Runin"
outPutfile = os.path.dirname(sys.argv[0]) + "/_runin_result.csv"
FilePath = "/Phoenix/Logs/processlog.plog"
DefaultFile = os.path.dirname(sys.argv[0]) + "/Unitsinfo.txt"

def writefile(string,file):
    try:
        with open(file, 'a') as d:
            d.write(string + '\n')
    except IOError as i:
        print ('IOError_4:',i)

def systemProfiler(types):
    systemProfilerXml=Popen(["system_profiler", types, "-xml"], stdout=PIPE).communicate()[0]
    pl=readPlistFromString(systemProfilerXml)
    return pl

def SP(types,item_to_check):
    return systemProfiler(types)[0]['_items'][0][item_to_check]

def Check_Fail(filePath):
    try:
        with open(filePath) as msg:
            for line in msg:
                if "FAIL-UPDA" in line:
                    a = line.split('"')[19]
                    b = line.split('"')[15]
                    c = line.split('"')[21].replace(',', '')
                    d = line.split('"')[-8]
                    tol = a + " #" + b + " " + c + " " + d
                    if a == "Core.Check.Config" or a == "Core.Check.ModelFirmware":
                        tol = line.split('"')[33].replace('.', '')
                    if c == "Device not found":
                        tol = a + " " + c
                    Set_1.append(tol)
            Set = set(Set_1)
            Set_2 = [ i for i in Set ]
            for le in Set_2:
                if "Passed on Retry" in le:
                    ae = le.replace('Passed on Retry', '')
                    Set_2.remove(le)
                    Set_2.remove(ae)
            return Set_2
    except IOError as e:
        print ('IOErro_1 :',e)

def Check_Default(file,Serial,Port):
    try:
        with open(file) as mg:
            for line in mg:
                if Serial in line:
                    try:
                        return line.split()[int(Port)]
                    except IndexError as c:
                        print ('IndexError:',c)
    except IOError as d:
        print ('IOError_2:',d)

def Bundle_Check(file):
    try:
        with open(file) as sg:
            for line in sg:
                if "DTI" in line:
                    ad = line.split('"')[15]
                    Set_3.append(ad)
            return Set_3[1]
    except IOError as f:
        print ('IOError_3:',f)

def Check_OutFile(file):
    try:
        if not os.path.isfile(file):
            title = "Unit Number, Serial Number, Config, Location, Error Message, Remark bundle"
            writefile(title,file)
    except TypeError as h:
        print ('TypeError_1:',h)

if __name__ == '__main__':
    Check_OutFile(outPutfile)
    SerialNumber = SP("SPHardwareDataType", 'serial_number')
    Config = Check_Default(DefaultFile,SerialNumber,3)
    UnitNumber = Check_Default(DefaultFile,SerialNumber,4)
    Bundle = Bundle_Check(FilePath)

    for l in Check_Fail(FilePath):
        A = str(UnitNumber) + "," + str(SerialNumber) + "," + str(Config) + "," + Location + "," + l + "," + Bundle
        writefile(A,outPutfile)