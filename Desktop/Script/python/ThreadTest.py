#!/usr/bin/env python
# -*- encoding:UTF-8 -*-

import time
import Queue
import threading
import random
import os
import re

q = Queue.Queue(0) #当有多个线程共享一个东西的时候就可以用它了
NUM_WORKERS = 3
n = 0

Path = "/Users/sasenyzhou/Documents/Nand_Command"

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
    global n
    #time.sleep(random.random() * 3)
    file = str(job)
    filename = file.replace('.gz','')
    os.system('gunzip %s %s &>/dev/null'%(file,Path))
    with open(filename) as dd:
        for line in dd:
            zued = re.findall(r'\bC02.*\'\b',line)
        if zued:
            print zued[0].replace('\'','')
    n = n + 1
    print "Processing: The " + str(n) + " Log ..."

    #print "doing",job," worktype ",worktype

if __name__ == '__main__':
    a = find_file(Path,".gz")
    print "begin...."
    for i in a:
       q.put(i) #放入到任务队列中去
    print "job qsize:",q.qsize()
    for x in range(NUM_WORKERS):
       MyThread(q,x).start()
