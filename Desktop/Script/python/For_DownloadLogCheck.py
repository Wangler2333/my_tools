#!/usr/bin/env python
# -*- encoding:UTF-8 -*-
# For SW_Download Log info Check
# Create by Saseny on 2017/05/10

import os
from shutil import copy
import glob
import re

def writefile(string,file):
    try:
        with open(file, 'a') as d:
            d.write(string + '\n')
    except IOError as i:
        print ('IOError:',i)

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
            print "Processing: The [" + str(n) + "] Log"
            copy(i,TempPath)
            os.system('gunzip ~/Downloads/temp/*')
            filepath = glob.glob(TempPath + '/*.log')
            SerialNumber = str(filepath[0]).split('/')[-1].split('_')[0]
            with open(str(filepath[0])) as fr:
                for line in fr:
                    d = re.findall(r'J79A_[A-Z][A-Z][A-Z]_[0-9]-[0-9]_[0-9]\..*\.dmg',line)
                    if d:
                        BundleName = d[0]
                    s = re.findall(r'\bC02.*;',line)
                    w = re.findall(r'\bC02.*\+.*\/.',line)
                    if s:
                        SerialNumber = s[0].replace(';','')
                    if w:
                        WIP = w[0]
                    cm = re.findall(r'\b\/.*694.*\.dmg\b',line)
                    if cm:
                        CMBundle = cm[0].split('/')[-1]
                    if "Overall =" in line:
                        Overall = line.split('=')[-1].split()[0]
                    if "Partition =" in line:
                        Partition = line.split('=')[-1].split()[0]
                    if "Test Image Restore =" in line:
                        Restore = line.split('=')[-1].split()[0]
                    if "CM Copy =" in line:
                        CMCopy = line.split('=')[-1].split()[0]
                    Time = re.findall(r'2017-[0-9][0-9]-[0-9][0-9] \[[0-9][0-9]\:[0-9][0-9]\:[0-9][0-9]\.[0-9][0-9][0-9]\]',line)
            #if Time:
                #print Time[0]
            result = str(Time[0]) + ',' + str(SerialNumber) + ',' + str(WIP) + ',' + str(BundleName) + ',' + str(CMBundle) + ',' + str(Partition) + ',' + str(Restore) + ',' + str(CMCopy) + ',' + str(Overall)
            writefile(str(result),ResultPath)
            os.system('rm -rf ~/Downloads/temp/*')
    except TypeError as e:
        print ('TypeError',e)

if __name__ == '__main__':
    LogPath = raw_input("请输入需要处理的Log的路径(生成结果在Documents文件夹内/'resultForLog.csv'):\n")
    TempPath = os.path.expanduser('~') + "/Downloads/temp"
    ResultPath = os.path.expanduser('~') + "/Documents/resultForLog.csv"
    if not os.path.isfile(ResultPath):
        string = "Time" + ',' + "Serial Number" + ',' + "WIP" + ',' + "Test Bundle" + ',' + "CM Bundle" + ',' + "Partition Time" + ',' + "Restore Time" + ',' + "CM Copy Time" + ',' + "Overall Time"
        writefile(string,ResultPath)
    if os.path.isdir(TempPath):
        os.system('rm -rf ~/Downloads/temp')
    os.mkdir(TempPath)
    Processing()