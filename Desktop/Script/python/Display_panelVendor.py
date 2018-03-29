#!/usr/bin/python
# -*- coding: UTF-8 -*-
# -*- coding: GBK -*-

'''
  Created by Saseny on 2017/06/05  (If found any issue pls contact with me and debug it, thanks!)

   For Time Calculate with processlog: (You can use for Run-in time check and others test time check.)
       1. Start parameter for check;
       2. End parameter for check;
       3. Will out put : Serial Number,CPU,Memory,SSD,Keyboard Country,Start Time,End Time,Used Time,Bundle Name,Memory Vendor;
       4. Default parameter : [Startparameter = "CM_Bundle_Verify"] / [Endparameter = "CM ASR _694"], you can change for others project;
       5. Only for J79A Run-in log check, if you want use for others project then need modify relate parameter;
       6. Default setup thread quantity was 10.

   Version:
       1. Version 1.0 on 2017/06/05;
'''

import time
import sys
import os
import Queue
import threading
import re
import glob
import csv

Startparameter = "CM_Bundle_Verify"
Endparameter = "CM ASR _694"

q = Queue.Queue(0)
NUM_WORKERS = 10
mylock = threading.Lock()

class MyThread(threading.Thread):
    def __init__(self,input,worktype):
        self._jobq = input
        self._work_type = worktype
        threading.Thread.__init__(self)
    def run(self):
        while True:
            if self._jobq.qsize() > 0:
                self._process_job(self._jobq.get(),self._work_type)
            else:
                break
    def _process_job(self, job, worktype):
        doJob(job,worktype)

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

def doJob(job, worktype):
    global Number
    file = str(job)
    filepath = os.path.dirname(file)
    os.system('cd %s ; tar -zxf %s &>/dev/null' % (filepath,file))
    FileName = file.replace('.tgz','')
    de = re.findall(r'C02.*\_.*', FileName)
    if de:
        SerialNumber = de[0].split('_')[0]
    r = glob.glob(FileName + '/*/processlog.plog')
    t = glob.glob(FileName + '/*/*/processlog.plog')
    Running = False
    if r:
        LogPoath = r[0]
        Running = True
    if t:
        LogPoath = t[0]
        Running = True
    if Running == True:
        print "Doing -- [" + str(SerialNumber) + "] --- Thread@ " + str(worktype) + " Start"
        mylock.acquire()
        Processing(LogPoath,FileName,SerialNumber)
        print "Done  -- [" + str(SerialNumber) + "] --- Thread@ " + str(worktype) + " End"
        os.system('rm -rf %s' % FileName)
        mylock.release()
    else:
        print "\033[0;31m" + "doing", FileName, " --- worktype Log Was Wrong -Thread@ ", str(worktype) + "\033[0m"
        os.system('rm -rf %s' % FileName)

def read_plog(filepath,fromt,pot):
    try:
        a = []
        e = []
        with open(filepath) as msg:
            for line in msg:
                if fromt in line:
                    time = re.findall(r'\"20[0-9][0-9]\/[0-9][0-9]\/[0-9][0-9] [0-9][0-9]\:[0-9][0-9]\:[0-9][0-9]\"',line)
                    if time:
                        a.append(time[0].split('\"')[1])
            if len(a) >= 1:
                if int(pot) == 1:
                    TIME = a[0]
                if int(pot) == 2:
                    TIME = a[-1]
                return TIME
            else:
                return e
    except UnboundLocalError as o:
        print ('UnboundLocalError',o)

def Time_chek(_time):
    try:
        timeArray = time.strptime(_time, "%Y/%m/%d %H:%M:%S")
        timeStamp = int(time.mktime(timeArray))
        return timeStamp
    except UnboundLocalError as p:
        print ('UnboundLocalError', p)

def Bundle_Check(file):
    try:
        b = []
        with open(file) as sg:
            for line in sg:
                if "DTI" in line:
                    ad = line.split('"')[15]
                    b.append(ad)
            return b[1]
    except IOError as f:
        print ('IOError_3:',f)

def check_Battery(filepath):
    try:
        c = []
        with open(filepath) as oi:
            for line in oi:
                if "InternalBattery" in line:
                    c.append(line.split()[2].replace(';',''))
            return c[1]
    except IOError as pp:
        print ('IOError',pp)

def Time_calculate(Start, End):
    d = int(End) - int(Start)
    hour = d / 3600
    d1 = d % 3600
    min = d1 / 60
    d2 = d1 % 60
    time = str(hour) + "h" + str(min) + "m" + str(d2) + "s"
    return time

def check_Memory_vonder(filepath):
    try:
        c = []
        with open(filepath) as gs:
            for line in gs:
                if "Memory" in line and "vendor:" in line:
                    c.append(line.split('"')[11].split(':')[-1])
            if len(c) >= 1:
                return str(c[0])
            else:
                return "None"
    except IOError as oi:
        print ('IOError', oi)

def config_check(path):
    try:
        K = "Apple Internal Keyboard / Trackpad"
        with open(path) as fe:
            for line in fe:
                if K in line:
                    KB = line.split('"')[3]
                if "Memory" in line:
                    MY = line.split('"')[1]
                if "devicecapacity" in line:
                    SD = line.split('"')[1]
                    if SD == 1000:
                        SD = 1024
                if "frequency" in line:
                    CPU = line.split('"')[3]
            return  CPU, MY, SD, KB
    except TypeError as po:
        print ('TypeError',po)

def Processing(LogPoath,FileName,SerialNumber):
    '''
    d = []

    if len(find_file(FileName, "configExpected.txt")) >= 1:
        ConfigFile = find_file(FileName, "configExpected.txt")[0]
        CPU, Memory, SSD, Keyboard = config_check(ConfigFile)
    else:
        CPU = "" ; Memory = "" ; SSD = "" ; Keyboard = ""

    if "_PRE_" not in FileName:
        Memory_vendor = check_Memory_vonder(LogPoath)
    else:
        Memory_vendor = ""

    Bundle = Bundle_Check(LogPoath)
    if len(read_plog(LogPoath, Startparameter,"1")) != 0 and len(read_plog(LogPoath, Endparameter,"2")) != 0:
        Startime = Time_chek(read_plog(LogPoath, Startparameter,"1"))
        Endtime = Time_chek(read_plog(LogPoath, Endparameter,"2"))
        Time = Time_calculate(Startime, Endtime)
    else:
        Time = ""

    d.append(str(SerialNumber))
    d.append(str(CPU))
    d.append(str(Memory))
    d.append(str(SSD))
    d.append(str(Keyboard))
    d.append(str(read_plog(LogPoath, Startparameter,"1")))
    d.append(str(read_plog(LogPoath, Endparameter,"2")))
    d.append(str(Time))
    d.append(str(Bundle))
    d.append(str(Memory_vendor))

    writer = csv.writer(open(Resultpath, 'a'))
    writer.writerow(d)
    '''

    with open(LogPoath) as ed:
        for line in ed:
            a = re.search('panelVendor="(.*?)"',line)
            if a:
                Vendor = a.group(1)
    reselt =  SerialNumber + ',' + str(Vendor)
    writefile(reselt,Resultpath)

if __name__ == '__main__':
    Path = raw_input("请输入Log路径: ")
    Date = time.strftime("%Y_%m_%d_%H_%M_%S")
    Resultpath = os.path.expanduser('~') + "/Desktop/" + Date + '.csv'
    print "\033[1;31m" + "结果路径: " + Resultpath + "\033[0m"
    if not os.path.isfile(Resultpath):
        red = "Serial Number" + ',' + "panelVendor"
        '''
        red = "Serial Number" + ',' + "CPU" + ',' + "Memory" + ',' + "SSD" + ','\
              + "Keyboard Country" + ',' + "Start Time" + ',' + "End Time" + ',' \
              + "Used Time" + ',' + "Bundle Name" + ','+ "Memory Vendor"
        '''
        writefile(red, Resultpath)
        print "Done"
    a = find_file(Path, ".tgz")
    print "Begin...."
    for i in a:
        q.put(i)
    print "Job Qsize:", q.qsize()
    for x in range(NUM_WORKERS):
        MyThread(q, x).start()