#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import sys
import commands
import time
from subprocess import Popen, PIPE
from plistlib import readPlistFromString
import matplotlib.pyplot as plt

def systemProfiler(types):
    systemProfilerXml=Popen(["system_profiler", types, "-xml"], stdout=PIPE).communicate()[0]
    pl=readPlistFromString(systemProfilerXml)
    return pl

def SP(types,item_to_check):
    return systemProfiler(types)[0]['_items'][0][item_to_check]

def writefile(string,file):
    try:
        with open(file, 'a') as d:
            d.write(string + '\n')
    except IOError as i:
        print ('IOError:',i)

def Matlib(parameter):
    global Mesg
    y_values = parameter
    a = len(parameter)
    x_values = list(range(a))
    plt.plot(x_values, y_values, linewidth=2)
    plt.ylim((0, 100))
    plt.title("Temperature changed", fontsize=20)
    plt.xlabel("Times", fontsize=14)
    plt.ylabel("Temperature", fontsize=14)
    plt.tick_params(axis='both', labelsize=14)
    plt.savefig('Temperature.png', bbox_inches='tight')
    plt.show()

def RunCheckTemp():
    global Times
    global TimeOut
    global cmd
    TempChange = []
    os.system('open -a /Applications/Utilities/Terminal.app %s'%cmd)
    for i in xrange(Times):
        Quit, Output = commands.getstatusoutput('ypc2 -drk TC0P')
        TempChange.append(str(Output))
        if i == 0:
            resultTemp = "初始CPU温度       " + str(Output) + " 度"
        else:
            resultTemp = "加热" + str(i*TimeOut) + "秒后CPU温度  " + str(Output) + " 度"
        print resultTemp
        writefile(resultTemp,Result)
        for j in xrange(TimeOut):
            time.sleep(1)
    os.system('killall -m vertexperf')
    Matlib(TempChange)

if __name__=='__main__':
    Times = int(raw_input("请输入需要测试的次数:"))
    TimeOut = int(raw_input("请输入测试时间间隔(s):"))
    Mesg = "QTY: " + str(Times) + " Time interval: " + str(TimeOut)
    SerialNumber = SP("SPHardwareDataType",'serial_number')
    if "C02" not in SerialNumber:
        with open("/Phoenix/Logs/SerialNumber.txt") as fo:
            for line in fo:
                SerialNumber = line
    cmd = os.path.dirname(sys.argv[0]) + '/TempCheck.sh'
    Result = os.path.expanduser('~') + "/Desktop/" + SerialNumber + '.txt'
    if not os.path.isfile(Result):
        ttm = "次数    " + "      " + "       温度"
        writefile(ttm, Result)
    RunCheckTemp()