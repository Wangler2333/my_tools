#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Creatr by Saseny on 2017/05/27
# For Control Run WIP Collect

import re
import os
import sys

Right = "正确"
Wrong = "错误"
Double = "重复"
End = "结束"

def writefile(string, file):
    try:
        with open(file, 'a') as d:
            d.write(string + '\n')
    except IOError as i:
        print ('IOError:', i)

def WIPCheck(wip):
    if wip == "217":
        #os.system('say %s' % End)
        print "\033[0;34m" + End + "\033[0m"
        os._exit(0)
    d = []
    Write = False
    CON = True
    with open(ResultPath) as fe:
        for line in fe:
            if "C02" in line:
               d.append(line)
        if wip + "\n" in d:
            CON = False
    Number = int(len(d)) + 1
    if "+" in wip:
        SerialNumber = str(wip).split('+')[0]
        ModelNumber = str(wip).split('+')[1]
        a = re.match('C02.*[A-Z]',SerialNumber)
        if a and len(SerialNumber) == 12 and ModelNumber:
            if CON == False:
                #os.system('say %s' % Double)
                print "\033[0;35m" + Double + "\033[0m"
                Write = False
            else:
                #os.system('say %s %s' % (Right,Number))
                print "\033[0;32m" + Right + str(Number) + "\033[0m"
                Write = True
        else:
            #os.system('say %s' % Wrong)
            print "\033[0;31m" + Wrong + "\033[0m"
            Write = False
    else:
        #os.system('say %s' % Wrong)
        print "\033[0;31m" + Wrong + "\033[0m"
        Write = False
    if Write == True:
        writefile(wip,ResultPath)

if __name__ == '__main__':
    ResultFileName = raw_input("请输入结果文件名:")
    ResultPath = os.path.dirname(sys.argv[0]) + '/' + str(ResultFileName) + ".csv"
    if not os.path.isfile(ResultPath):
        s = "Control Run WIP Collect:"
        writefile(s,ResultPath)
    while True:
        WIP = raw_input("请扫入WIP: ")
        WIPCheck(WIP)
