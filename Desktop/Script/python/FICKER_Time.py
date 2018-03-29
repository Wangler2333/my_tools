#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import os
import glob
import shutil
import plistlib

temp = os.path.dirname(sys.argv[0]) + '/temp'
plistPath = os.path.dirname(sys.argv[0]) + '/Flicker.plist'
ResultFile= os.path.dirname(sys.argv[0]) + '/Flicker_time.csv'


def writefile(string,file):
    try:
        with open(file, 'a') as d:
            d.write(string + '\n')
    except IOError as i:
        print ('IOError:',i)

def ReadPlist(plistPath):
    Dic = plistlib.readPlist(plistPath)
    return Dic

def ReadLog(filepath):
    b = {}
    filename = os.path.basename(filepath)
    SerialNmber = filename.split('_')[0]
    with open(filepath) as e:
        for line in e:
            if ":" in line:
                b[line.split()[0]] = line.split()[-1]
        total1 = float(b['0'])+float(b['1'])+float(b['2'])+float(b['3'])+float(b['4'])+float(b['5'])+float(b['6'])
        total2 = float(b['7'])+float(b['8'])+float(b['9'])+float(b['10'])+float(b['11'])+float(b['12'])
        total = total1+total2
        result = SerialNmber,b['0'],b['1'],b['2'],b['3'],b['4'],b['5'],b['6'],b['7'],b['8'],b['9'],b['10'],b['11'],b['12'],total
        print result

def unzip_Log(LogPath):
    try:
        fns = [os.path.join(root, fn) for root, dirs, files in os.walk(LogPath) for fn in files]
        for f in fns:
            if os.path.isfile(f):
                if ".zip" in f:
                    os.system('/Users/saseny/Desktop/Flicker_Test/Script/mkdir_temp.sh')
                    shutil.copy(f,temp)
                    os.system('/Users/saseny/Desktop/Flicker_Test/Script/unzip_log.sh')
                    file_ = temp + '/*_CycleTime.txt'
                    ReadLog(glob.glob(file_))
                    os.system('/Users/saseny/Desktop/Flicker_Test/Script/rm_temp.sh')

    except IOError as o:
        print ('IOError', o)

def CheckFile():
    os.system('/Users/saseny/Desktop/Flicker_Test/Script/rm_temp.sh')
    if not os.path.isfile(ResultFile):
        a1 = str(ReadPlist(plistPath)['0'][1]) + ',' + str(ReadPlist(plistPath)['1'][1]) + ',' + str(
            ReadPlist(plistPath)['2'][1]) + ',' + str(ReadPlist(plistPath)['3'][1])
        a2 = str(ReadPlist(plistPath)['4'][1]) + ',' + str(ReadPlist(plistPath)['5'][1]) + ',' + str(
            ReadPlist(plistPath)['6'][1]) + ',' + str(ReadPlist(plistPath)['7'][1])
        a3 = str(ReadPlist(plistPath)['8'][1]) + ',' + str(ReadPlist(plistPath)['9'][1]) + ',' + str(
            ReadPlist(plistPath)['10'][1]) + ',' + str(ReadPlist(plistPath)['11'][1]) + ',' + str(
            ReadPlist(plistPath)['12'][1])
        ab = "SerialNumber" + ',' + a1 + ',' + a2 + ',' + a3 + ',' + "Total"
        writefile(str(ab), ResultFile)

if __name__ == '__main__':
    CheckFile()
    LogPath = raw_input("请输入Log路径:")
    unzip_Log(LogPath)
