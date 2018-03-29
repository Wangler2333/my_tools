#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For J80a run in log check
# Create by Saseny on 2017/06/28

import threading
import Queue
import os
import re
import glob
import time

q = Queue.Queue(0)
NUM_WORKERS = 10
mylock = threading.Lock()
Check_Start = "system_profiler SPPowerDataType"
Check_End = "Load_unload_plist.sh"


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


def writefile(string, file):
    try:
        with open(file, 'a') as d:
            d.write(string + '\n')
    except IOError as i:
        print ('IOError:', i)


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


def check_Memory_vonder(filepath):
    try:
        c = []
        with open(filepath) as gs:
            for line in gs:
                if "Memory" in line and "vendor:" in line:
                    c.append(line.split('"')[11].split(':')[-1])
            if c:
                return str(c[0])
            else:
                return None
    except IOError as oi:
        print ('IOError', oi)


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


def doJob(job, worktype):
    global Number
    file = str(job)
    filepath = os.path.dirname(file)
    os.system('cd %s ; tar -zxf %s &>/dev/null' % (filepath, file))
    FileName = file.replace('.tgz', '')
    de = re.findall(r'C02[A-Z]\w{8}', FileName)
    if de:
        SerialNumber = de[0]
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
        # print "doing", LogPoath, " --- Thread@ " + str(worktype) + " Start"
        print "Doing -- [" + str(SerialNumber) + "] --- Thread@ " + str(worktype) + " Start"
        mylock.acquire()
        Processing(LogPoath, SerialNumber)
        # print "doing", LogPoath, " --- Thread@ " + str(worktype) + " End"
        print "Done  -- [" + str(SerialNumber) + "] --- Thread@ " + str(worktype) + " End"
        os.system('rm -rf %s' % FileName)
        mylock.release()
    else:
        print "\033[0;31m" + "doing", FileName, " --- worktype Log Was Wrong -Thread@ ", str(worktype) + "\033[0m"
        # print "\033[0;31m" + "Doing -- [" + str(SerialNumber) + "] --- worktype Log Was Wrong -Thread@ ", str(worktype) + "\033[0m"
        os.system('rm -rf %s' % FileName)


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
        print ('IOError_3:', f)


def Processing(filename, sn):
    try:
        time_start = []
        time_end = []
        with open(filename) as f:
            for line in f:
                if Check_Start in line:
                    Time1 = re.findall(r'[0-9]{4}/[0-9]{2}/[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}', line)
                    if len(Time1) > 0:
                        time_start.append(Time1[0])
                if Check_End in line:
                    Time2 = re.findall(r'[0-9]{4}/[0-9]{2}/[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}', line)
                    if len(Time2) > 0:
                        time_end.append(Time2[0])

        time_left = Time_calculate(Time_chek(time_start[-1]), Time_chek(time_end[-1]))
        check_memory = check_Memory_vonder(filename)
        bundle_name = Bundle_Check(filename)

        result = str(sn) + ',' + str(bundle_name) + ',' + str(check_memory) + ',' + str(time_left)
        writefile(result, Resultpath)

    except TypeError as e:
        print('UnboundLocalError', e)


if __name__ == '__main__':
    Path = raw_input("请输入Log路径:")
    Date = time.strftime("%Y_%m_%d_%H_%M_%S")
    Resultpath = os.path.expanduser('~') + '/Downloads/' + Date + '.csv'
    print "\033[1;31m" + "结果路径: " + Resultpath + "\033[0m"
    if not os.path.isfile(Resultpath):
        red = "Serial Number" + ',' + "Bundle Name" + ',' + "Memorry Vendor" + ',' + "Left Time"
        writefile(red, Resultpath)
    a = find_file(Path, ".tgz")
    print "Begin...."
    for i in a:
        q.put(i)
    print "Job Qsize:", q.qsize()
    for x in range(NUM_WORKERS):
        MyThread(q, x).start()
