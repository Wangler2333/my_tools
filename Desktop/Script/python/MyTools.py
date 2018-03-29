#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# __author__: Saseny Zhou


import sys
import os
import threading
import Queue
import re
import glob
import thread

reload(sys)
sys.setdefaultencoding('utf-8')

q = Queue.Queue(0)
p = Queue.Queue(0)

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


class MyTools(object):
    def __init__(self, LogPath=None, suffix=None):
        self.logPath = LogPath
        self.suffix = suffix

    def findFile(self):
        try:
            findList = []
            fns = [os.path.join(root, fn) for root, dirs, files in os.walk(self.logPath) for fn in files]
            for f in fns:
                if os.path.isfile(f):
                    if self.suffix in f:
                        findList.append(f)
            return findList
        except IOError as o:
            print('IOError', o)

    def unTgzFile(self, file):

        if os.path.isfile(file):

            path = os.path.dirname(file)
            os.system('cd %s ; tar -zxf %s &>/dev/null' % (path, file))
            pathName = str(file).replace('.tgz', '')

            t = re.findall(r'C02[A-Z]\w{8}', os.path.basename(file))
            if len(t) > 0:
                serialnumber = t[0]
            else:
                serialnumber = 'None'

            passPath = glob.glob(pathName + '/*/processlog.plog')
            failPath = glob.glob(pathName + '/*/*/processlog.plog')

            if passPath:
                content = self.readFile(passPath[0])
                p.put(content)

            elif failPath:
                content = self.readFile(passPath[0])
                p.put(content)

            os.system('rm -rf %s' % pathName)
        else:
            print(file + ': 文件路径不存在')

    def readFile(self, file):
        try:
            f = open(file, 'r')
            f_obj = f.readlines()
            f.close()
            return f_obj
        except:
            pass


def doJob(job, worktype):
    d = re.findall(r'C02[A-Z]\w{8}', job)
    if len(d) > 0:
        serialnumber = d[0]
    else:
        serialnumber = 'None'

    print 'Starting  -- >> [%s]  -- Thread %i' % (serialnumber, int(worktype))
    t.unTgzFile(job)


def queceAdd(list):
    for i in list:
        q.put(i)
    print "Job Qsize:", q.qsize()
    for x in range(NUM_WORKERS):
        MyThread(q, x).start()


def printGet(info):
    for i in info:
        print str(i).replace('\n','')


if __name__ == '__main__':
    t = MyTools()
    t.logPath = '/Users/saseny/Desktop/LOGS/Test'
    t.suffix = '.tgz'
    list = t.findFile()
    queceAdd(list)

    while True:

        mylock.acquire()
        a = p.get()
        thread.start_new_thread(printGet,(a,))
        mylock.release()

        if q.qsize() == 0 and p.qsize() == 0:
            break
