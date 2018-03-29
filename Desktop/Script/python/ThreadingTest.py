#!/usr/bin/python
# -*- coding: UTF-8 -*-

import time
import Queue
import threading
import random
import os
import re
import glob

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

def doJob(job, worktype):
    file = str(job)
    os.system('cd %s ; tar -xzf %s &>/dev/null' % (Path,file))
    os.system('sleep 5')
    filename = file.replace('.tgz', '')

    Runner = False
    if glob.glob(filename + '/*/processlog.plog'):
        LogPath = glob.glob(filename + '/*/processlog.plog')[0]
        Runner = True
    if glob.glob(filename + '/*/*/processlog.plog'):
        LogPath = glob.glob(filename + '/*/*/processlog.plog')[0]
        Runner = True

    mylock.acquire()
    if Runner == True:
        Processing(LogPath)
        print "doing", job, " --- worktype ", worktype
    else:
        print "-- This %s Log was wrong. --- worktype %s"%(filename,worktype)
    os.system('rm -rf %s'%filename)

    mylock.release()

def Processing(Path):
    SerialNumber = str(Path).split('/')[5].split('_')[0]
    with open(str(Path)) as fr:
        for line in fr:
            d = re.findall(r'J79A_[A-Z][A-Z][A-Z]_[0-9]-[0-9]_[0-9]\..*\.dmg', line)
            if d:
                BundleName = d[0]
            s = re.findall(r'\bC02.*;', line)
            w = re.findall(r'\bC02.*\+.*\/.', line)
            if s:
                SerialNumber = s[0].replace(';', '')
            if w:
                WIP = w[0]
            cm = re.findall(r'\b\/.*694.*\.dmg\b', line)
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
    result = str(Time[0]) + ',' + str(SerialNumber) + ',' + str(WIP) + ',' + str(BundleName) + ',' + str(CMBundle) + ',' + str(Partition) + ',' + str(Restore) + ',' + str(CMCopy) + ',' + str(Overall)
    writefile(str(result),Resultpath)

if __name__ == '__main__':
    q = Queue.Queue(0)
    NUM_WORKERS = 5
    mylock = threading.Lock()
    Resultpath = "/Users/saseny/Desktop/SN_List/123.log"
    if not os.path.isfile(Resultpath):
        red = "Time" + ',' + "Serial Number" + ',' + "WIP" + ',' + "Test Bundle" + ',' + "CM Bundle" + ',' + "Partition Time" + ',' + "Restore Time" + ',' + "CM Copy Time" + ',' + "Overall Time"
        writefile(red,Resultpath)
    Path = raw_input("Pls input Path:")
    os.system('open %s' % Resultpath)
    a = find_file(Path,".tgz")
    print "begin...."
    for i in a:
        q.put(i)
    print "job qsize:",q.qsize()
    for x in range(NUM_WORKERS):
        MyThread(q,x).start()
        q.join()
