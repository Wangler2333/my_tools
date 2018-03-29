#!/usr/bin/env python
# coding: UTF-8

import time
import Queue
import threading
import random
import os
import re
import glob

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
    SN = str(job)
    b = find_file(path3, ".log.gz")
    for i in b:
        str(i).split('/')[-1].split('_')[0]



    print "-- This %s Log was wrong. --- worktype %s"%(job,worktype)

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

if __name__ == '__main__':
    q = Queue.Queue(0)
    NUM_WORKERS = 20
    mylock = threading.Lock()
    path1 = "/Users/saseny/Desktop/4_13__.txt"
    path2 = "/Users/saseny/Desktop/DDDDDD.txt"
    path3 = "/Users/saseny/Downloads/05_17_2017_09_46_AM"
    a = []
    with open(path1) as fe:
        for line in fe:
            a.append(line)
    print "begin...."
    for i in a:
        q.put(i)
    print "job qsize:",q.qsize()
    for x in range(NUM_WORKERS):
        MyThread(q,x).start()
        q.join()