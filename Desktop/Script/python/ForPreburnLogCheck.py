#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# For Pre-burn Log Box SN Check whether flow AAB Test
# Created by Saseny on 2017/5/22
# Base on 1.0 Add parameter check whether output box serial number list with result file
#      -- If no parameter input before command running then no box serial number list output.
#      -- Any parameter can enable it with box serial number list output.
# Version 1.1

import threading
import Queue
import os
import re
import glob
import csv
import sys

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
            p = []
            d = []
            for line in ae:
                f = re.findall(r'C02.*\+.*\,',line)
                if f:
                    SerialNumber = f[0].split('+')[0]
                b = re.findall(r'J79A_.*_[0-9]-[0-9]_[0-9]\..*\,',line)
                if b:
                    BundleName = b[0].split('"')[0]
                xs = re.findall(r'Serial\(FAPX.*\) \-',line)
                if xs:
                    p.append(xs[0].split('(')[1].split(')')[0])
                ps = re.findall(r'Serial Number\: FAPP.*\"\,',line)
                if ps:
                    d.append(ps[0].split(':')[1].replace('",',''))

            RESULT = []
            RESULT.append("Box SN List: ")
            #RESULT.append("")
            Xenon = "Xenon: " + str(len(p))
            RESULT.append(Xenon)
            RESULT1 = RESULT + p
            Palladium = "Palladium: " + str(len(d))
            RESULT1.append(Palladium)
            RESULT2 = RESULT1 + d

            XenonBox1 = set(p)
            XenonBox = []
            for o in XenonBox1:
                XenonBox.append(o)
            Palladium1 = set(d)
            PalladiumBox = []
            for p in Palladium1:
                PalladiumBox.append(p)

            Master = []
            Master.append(SerialNumber)
            Master.append(BundleName)
            Xenon_ = "Xenon: " + str(len(XenonBox))
            Master.append(Xenon_)
            Master_ = Master + XenonBox
            Palladium_ = "Palladium: " + str(len(PalladiumBox))
            Master_.append(Palladium_)
            MasterEnd = Master_ + PalladiumBox

            writer = csv.writer(open(Resultpath, 'a'))
            writer.writerow(MasterEnd)
            if len(sys.argv) == 2:
                writer.writerow(RESULT2)

        except TypeError as e:
            print('UnboundLocalError', e)

if __name__ == '__main__':
    Path = raw_input("请输入Log路径:")
    MaxTimes = raw_input("请输入处理Log线程数:")
    q = Queue.Queue(0)
    NUM_WORKERS = int(MaxTimes)
    mylock = threading.Lock()

    Resultpath = os.path.expanduser('~') + '/Documents/PreburnBoxCheck.csv'
    if not os.path.isfile(Resultpath):
        red = "Serial Number" + ',' + "Test Bundle"
        writefile(red, Resultpath)
    a = find_file(Path, ".tgz")
    print "begin...."
    for i in a:
        q.put(i)
    print "job qsize:", q.qsize()
    for x in range(NUM_WORKERS):
        MyThread(q, x).start()

