#!/usr/bin/env python
# -*- encoding:UTF-8 -*-
# For Nand Log test time calculate
# Create by Saseny on 2017/05/10
# Add SSD Capacity check

import os, sys
from shutil import copy
import time
import glob
import re

def writefile(string,file):
    try:
        with open(file, 'a') as d:
            d.write(string + '\n')
    except IOError as i:
        print ('IOError:',i)

def Time_chek(_time):
    try:
        timeArray = time.strptime(_time, "%Y/%m/%d %H:%M:%S")
        timeStamp = int(time.mktime(timeArray))
        return timeStamp
    except UnboundLocalError as p:
        print ('UnboundLocalError', p)

def Time_calculate(Start, End):
    try:
        d = int(End) - int(Start)
        hour = d / 3600
        d1 = d % 3600
        min = d1 / 60
        d2 = d1 % 60
        time = str(hour) + "h" + str(min) + "m" + str(d2) + "s"
        return time
    except UnboundLocalError as q:
        print ('UnboundLocalError', q)

def find_file(path,formet):
    try:
        a = []
        fns = [os.path.join(root, fn) for root, dirs, files in os.walk(path) for fn in files]
        for f in fns:
            if os.path.isfile(f):
                if formet in f:
                    a.append(f)
        return a
    except IOError as o:
        print ('IOError',o)

def Processing():
    try:
        n =0
        for i in find_file(LogPath,".gz"):
            n = n + 1
            times = []
            print "Processing: The [" + str(n) + "] Log"
            copy(i,TempPath)
            os.system('gunzip ~/Downloads/temp/*')
            filepath = glob.glob(TempPath + '/*.log')
            SerialNumber = str(filepath[0]).split('/')[-1].split('_')[0]
            with open(str(filepath[0])) as fe:
                for line in fe:
                    c = re.findall(r'2017-[0-9][0-9]-[0-9][0-9] [0-9][0-9]:[0-9][0-9]:[0-9][0-9]', line)
                    if "MBP" in line:
                        BootRom = line.split()[-1].replace('\'','')
                    if "SSD_CAPACITY" in line:
                        SSD_ = line.split('=')[1].split()
                    times.append(str(c).replace('-','/'))
            StartTime = Time_chek(str(times[0]).split('\'')[1])
            EndTime = Time_chek(str(times[-1]).split('\'')[1])
            LeftTime = Time_calculate(StartTime,EndTime)
            SSDCapacity = str(SSD_).split('\'')[1]
            result = SerialNumber + ',' + BootRom + ',' + str(SSDCapacity) + ',' + LeftTime
            writefile(str(result),ResultPath)
            os.system('rm -rf ~/Downloads/temp/*')
    except TypeError as e:
        print ('TypeError',e)

if __name__ == '__main__':
    LogPath = raw_input("请输入需要处理的Log的路径(生成结果在Documents文件夹内/'resultForNand.csv'):\n")
    TempPath = os.path.expanduser('~') + "/Downloads/temp"
    ResultPath = os.path.expanduser('~') + "/Documents/resultForNand.csv"
    if not os.path.isfile(ResultPath):
        string = "Serial Number" + ',' + "BootRom Version" + ',' + "SSD Capacity" +',' + "Left Time"
        writefile(string,ResultPath)
    if os.path.isdir(TempPath):
        os.system('rm -rf ~/Downloads/temp')
    os.mkdir(TempPath)
    Processing()