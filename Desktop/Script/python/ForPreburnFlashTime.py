#!/usr/bin/env python
# -*- encoding:UTF-8 -*-
# For Preburn Flash Station Test time calculate
# Created by Saseny on 2017/05/24
# Before Get time : Update Firmware used time
# After Get time : Restore M8 and Nvram set and quick test used time

import threading
import Queue
import os
import re
import glob
import time

q = Queue.Queue(0)
NUM_WORKERS = 10
mylock = threading.Lock()

class MyThread(threading.Thread):
    def __init__(self, input, worktype):
        self._jobq = input
        self._work_type = worktype
        threading.Thread.__init__(self)
    def run(self):
        while True:
            if self._jobq.qsize() > 0:
                self._process_job(self._jobq.get(), self._work_type)
            else:
                break
    def _process_job(self, job, worktype):
        doJob(job, worktype)

def Time_chek(_time):
    try:
        timeArray = time.strptime(_time, "%Y/%m/%d %H:%M:%S")
        timeStamp = int(time.mktime(timeArray))
        return timeStamp
    except UnboundLocalError as p:
        print ('UnboundLocalError', p)

def Time_calculate(Start, End):
    d = int(End) - int(Start)
    hour = d / 3600
    d1 = d % 3600
    min = d1 / 60
    d2 = d1 % 60
    time = str(hour) + "h" + str(min) + "m" + str(d2) + "s"
    return time

def writefile(string, file):
    try:
        with open(file, 'a') as d:
            d.write(string + '\n')
    except IOError as i:
        print ('IOError:', i)

def find_file(path, formet):
    try:
        a = []
        fns = [os.path.join(root, fn) for root, dirs, files in os.walk(path) for fn in files]
        for f in fns:
            if os.path.isfile(f):
                if formet in f:
                    a.append(f)
        return a
    except IOError as o:
        print ('IOError', o)

def TotalTimeCalculate(time1,time2):
    s1 = str(time1).split('m')[1].split('s')[0]
    s2 = str(time2).split('m')[1].split('s')[0]
    m1 = str(time1).split('h')[1].split('m')[0]
    m2 = str(time2).split('h')[1].split('m')[0]
    h1 = str(time1).split('h')[0]
    h2 = str(time1).split('h')[0]
    s_ = (int(s1) + int(s2)) / 60
    s = (int(s1) + int(s2)) % 60
    m_ = (int(m1) + int(m2) + int(s_)) / 60
    m = (int(m1) + int(m2) + int(s_)) % 60
    h = int(h1) + int(h2) + int(m_)
    time = str(h) + "h" + str(m) + "m" + str(s) + "s"
    return time

def doJob(job, worktype):
    file = str(job)
    os.system('cd %s ; tar -zxf %s &>/dev/null' % (Path,file))
    FileName = file.replace('.tgz','')
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
        print "doing", LogPoath, " --- Thread@ " + str(worktype) + " Start"
        mylock.acquire()
        Processing(LogPoath)
        print "doing", LogPoath, " --- Thread@ " + str(worktype) + " End"
        os.system('rm -rf %s' % FileName)
        mylock.release()
    else:
        print "doing", FileName, " --- worktype Log Was Wrong -Thread@ ", worktype
        os.system('rm -rf %s' % FileName)

def Processing(filename):
    with open(filename) as ae:
        try:
            SerialNumber = "None"
            BundleName = "None"
            Time1 = []
            Time4 = []
            for line in ae:
                f = re.findall(r'C02.*\+.*\,',line)
                if f:
                    SerialNumber = f[0].split('+')[0]
                b = re.findall(r'J.*_.*_[0-9]-[0-9]_[0-9]\..*\,',line)
                if b:
                    BundleName = b[0].split('"')[0]
                if MyParameter in line:
                   t = re.findall(r'20[0-9][0-9]\/[0-9][0-9]\/[0-9][0-9] [0-9][0-9]\:[0-9][0-9]\:[0-9][0-9]',line)
                   if t:
                       Time1.append(t[0])
                if MyParameter1 in line:
                    t1 = re.findall(r'20[0-9][0-9]\/[0-9][0-9]\/[0-9][0-9] [0-9][0-9]\:[0-9][0-9]\:[0-9][0-9]',line)
                    t2 = re.findall(r'[0-9][0-9]\-[0-9][0-9]\-20[0-9][0-9] [0-9][0-9]\:[0-9][0-9]\:[0-9][0-9]',line)
                    time_ = str(t2[0]).split()[0]
                    mouth = str(time_).split('-')[0]
                    day = str(time_).split('-')[1]
                    year = str(time_).split('-')[2]
                    date0 = year + '/' + mouth + '/' + day
                    time0 = str(t2[0]).split()[1]
                    Time3 = date0 +  " " + time0
                if MyParameter2 in line:
                    t3 = re.findall(r'20[0-9][0-9]\/[0-9][0-9]\/[0-9][0-9] [0-9][0-9]\:[0-9][0-9]\:[0-9][0-9]',line)
                    if t3:
                        Time4.append(t3[0])
            BeforeTime =  Time_calculate(Time_chek(Time1[0]),Time_chek(t1[0]))
            AfterTime = Time_calculate(Time_chek(Time3),Time_chek(Time4[0]))
            TotalTime = TotalTimeCalculate(BeforeTime,AfterTime)
            REsult = str(SerialNumber) + ',' + str(BundleName) + ',' + str(BeforeTime) + ',' + str(AfterTime) + ',' + str(TotalTime)
            writefile(REsult,Resultpath)
        except TypeError as e:
            print('UnboundLocalError', e)

if __name__ == '__main__':
    Path = raw_input("请输入Log路径:")

    MyParameter1 = "Setting time on"
    MyParameter2 = "USBC VBus to CC Pin Short Test"
    MyParameter = "PHNX-STAR"

    Resultpath = os.path.expanduser('~') + '/Documents/PreburnFlashTime.csv'
    if not os.path.isfile(Resultpath):
        red = "Serial Number" + ',' + "Test Bundle" + ',' + "Before Get Time" + ',' + "After Get Time" + ',' + "Total Time"
        writefile(red, Resultpath)
    a = find_file(Path, ".tgz")
    print "begin...."
    for i in a:
        q.put(i)
    print "job qsize:", q.qsize()
    for x in range(NUM_WORKERS):
        MyThread(q, x).start()
