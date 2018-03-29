#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Create by Saseny on 2017/07/21

import sys
import plistlib
import threading
import Queue
import os
import re
import glob
import time
import csv
import matplotlib


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


def doJob(job, worktype):
    file_path = str(job)
    filepath = os.path.dirname(file_path)
    log_folder_name = file_path.replace('.tgz', '')
    Running = False
    SerialNumber = ""
    processlog_path = ""

    os.system('cd %s ; tar -zxf %s &>/dev/null' % (filepath, file_path))

    serial_number = re.findall(r'C02[A-Z]\w{8}', log_folder_name)

    if len(serial_number) > 0:
        SerialNumber = serial_number[0]

    pass_log_path = glob.glob(log_folder_name + '/*/processlog.plog')
    fail_log_path = glob.glob(log_folder_name + '/*/*/processlog.plog')

    if len(pass_log_path) > 0:
        processlog_path = pass_log_path[0]
        Running = True
    if len(fail_log_path) > 0:
        processlog_path = fail_log_path[0]
        Running = True
    if "CQA" in processlog_path:
        Running = False

    if Running == True:

        print "Doing -- [" + str(SerialNumber) + "]" \
                                                 " --- Thread@ " + str(worktype) + " Start"
        mylock.acquire()
        Processing(processlog_path, SerialNumber, log_folder_name)
        print "Done  -- [" + str(SerialNumber) + "]" \
                                                 " --- Thread@ " + str(worktype) + " End"
        os.system('rm -rf %s' % log_folder_name)

        mylock.release()
    else:
        print "\033[0;31m" + "doing", log_folder_name, "" \
                                                       " --- worktype Log Was Wrong -Thread@ ", str(
            worktype) + "\033[0m"
        os.system('rm -rf %s' % log_folder_name)


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


def Processing(a,b,c):
    pass

if __name__ == '__main__':
    Path = raw_input("请输入Log路径:")
    log_list = find_file(Path, ".tgz")
    print "Begin...."
    for i in log_list:
        q.put(i)
    print "Job Qsize:", q.qsize()
    for x in range(NUM_WORKERS):
        MyThread(q, x).start()