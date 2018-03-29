#!/usr/bin/python
# -*- coding: UTF-8 -*-
# For Download Log Check
# Greated on 2017/5/17

import Queue
import threading
import os
import re

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
    file = str(job)
    os.system('gunzip %s &>/dev/null' % (file))
    filename = file.replace('.gz', '')
    mylock.acquire()
    print "doing", filename, " --- worktype ", worktype
    Processing(filename)
    print "doing", filename, " --- worktype ", worktype
    os.system('rm -rf %s'%filename)
    mylock.release()   

def Processing(filename):
    SerialNumber = str(filename).split('/')[-1].split('_')[0]
    with open(filename) as ae:
        try:
            BundleName = "None"
            CMBundle = "None"
            TimeStart = "None"
            TotalTime = "None"
            WIP = "None"
            for line in ae:
                if ".dmg" in line and "J79A" in line:
                    BundleName = line.split('/')[-1].split('.dmg')[0]
                d = re.findall(r'\[.*\.dmg\]',line)
                if d:
                    CMBundle = d[0].split('[')[2].replace(']','')
                t = re.findall(r'201[0-9]-[0-9][0-9]-[0-9][0-9] \[[0-9][0-9]\:[0-9][0-9]\:[0-9][0-9]\.[0-9][0-9][0-9]\]',line)
                if t:
                    TimeStart = t[0] #.split('.')[0].replace('[','')
                if "Overall" in line:
                    TotalTime = line.split('=')[1]
                w = re.findall(r'C02.*\+.*\"',line)
                if w:
                    WIP = w[0].replace('"','')
            result = str(TimeStart) + ',' + str(SerialNumber) + ',' + str(WIP) + ',' + str(BundleName) + ',' + str(CMBundle) + ',' + str(TotalTime)
            writefile(str(result),Resultpath)
        except UnboundLocalError as e:
            print('UnboundLocalError',e)
    
if __name__ == '__main__':
    Path = raw_input("请输入Log路径:")
    MaxTimes = raw_input("请输入处理Log线程数:")
    q = Queue.Queue(0)
    NUM_WORKERS = int(MaxTimes)
    mylock = threading.Lock()

    Resultpath= os.path.expanduser('~') + '/Documents/DownloadLogCheck.csv'
    if not os.path.isfile(Resultpath):
        red = "Time" + ',' + "Serial Number" + ',' + "WIP" + ',' + "Test Bundle" + ',' + "CM Bundle" + ',' + "Download Time"
        writefile(red,Resultpath)
    a = find_file(Path,".gz")
    print "begin...."
    for i in a:
        q.put(i)
    print "job qsize:",q.qsize()
    for x in range(NUM_WORKERS):
        MyThread(q,x).start()     