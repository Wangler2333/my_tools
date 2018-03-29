#!/usr/bin/python
# -*- coding: UTF-8 -*-

import time, datetime
import sys
import os
import shutil

a = []
b = []
c = []

def Check_OutFile(file):
    try:
        if not os.path.isfile(file):
            title = "SerialNumber,Time"
            writefile(title,file)
    except TypeError as h:
        print ('TypeError_1:',h)

def Time_chek(_time):
    try:
        timeArray = time.strptime(_time, "%Y/%m/%d %H:%M:%S")
        timeStamp = int(time.mktime(timeArray))
        return timeStamp
    except UnboundLocalError as p:
        print ('UnboundLocalError',p)

def Time_calculate(Start,End):
    d = Time_chek(int(End)) - Time_chek(int(Start))
    hour = d / 3600
    d1 = d % 3600
    min = d1 / 60
    d2 = d1 % 60
    time = str(hour) + "h" + str(min) + "m" + str(d2) + "s"
    return time

def move(source,target):
    shutil.copy(source,target)

def find_file(path,formet):
    try:
        fns = [os.path.join(root, fn) for root, dirs, files in os.walk(path) for fn in files]
        for f in fns:
            if os.path.isfile(f):
                if formet in f:
                    return f
    except IOError as o:
        print ('IOError',o)

def read_plog(filepath,fromt):
    try:
        with open(filepath) as msg:
            for line in msg:
                if fromt in line:
                    a.append(line.split('"')[3])
                    TIME = a[0]
                #if  Check_End in line:
                #    b.append(line.split('"')[3])
                #    endTime = b[-1]
            return TIME
    except UnboundLocalError as o:
        print ('UnboundLocalError',o)

def writefile(string,file):
    try:
        with open(file, 'a') as d:
            d.write(string + '\n')
    except IOError as i:
        print ('IOError_4:',i)

def Search(path, fromt):
    fns = [os.path.join(root, fn) for root, dirs, files in os.walk(path) for fn in files]
    for f in fns:
        if os.path.isfile(f):
            if fromt in f:
                try:
                    if "PASS" in f or "FAIL" in f:
                        Basename = os.path.basename(f)
                        SerialNumber = Basename.split('_')[0]
                        print SerialNumber

                        os.system('mkdir -p ~/Downloads/temp')
                        target_Path = os.path.expanduser('~') + "/Downloads/temp"
                        move(f,target_Path)

                        os.system('cd ~/Downloads/temp; tar -xzf * &>/dev/null')
                        Startime = read_plog(find_file(target_Path,".plog"),Check_Start)
                        Endtime = read_plog(find_file(target_Path,".plog"),Check_End)
                        Time = Time_calculate(Startime,Endtime)

                        result = SerialNumber + "," + Time
                        writefile(result,result_file)
                        os.chdir(os.path.dirname(sys.argv[0]))
                        os.system('a=`dirname $0` ; rm -rf $a/temp')
                except IOError as o:
                    print ('IOError',o)




Check_Start = "CM_Bundle_Verify"
Check_End = "Color_Cal_J79_0_native_flash"
# processlog = raw_input("Pls input file path:")
#logpath = "/Users/saseny/Desktop/03_16_2017_12_07_PM"

#result_file = os.path.expanduser('~') + "/Downloads/time_result.csv"
#Check_OutFile(result_file)
#if os.path.isdir(os.path.dirname(sys.argv[0]) + "/temp"):
#    os.system('a=`dirname $0` ; rm -rf $a/temp')
#Search(logpath,".tgz")
print read_plog("/Users/saseny/Desktop/C02T200YHT7H_RUNIN_PASS_2017_03_19@15_10_09/_PHOENIX_LOGS/Logs/processlog.plog",Check_End)
#2017/03/17 21:37:29
#2017/03/19 14:04:22