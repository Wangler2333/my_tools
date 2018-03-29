#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time     : 2017/11/29下午6:05
# @Author   : Saseny Zhou
# @Site     : 
# @File     : myThread.py
# @Software : PyCharm Community Edition

import threading
import Queue
from readcsv import *
from shell import *
import re
import plistlib
from collections import OrderedDict
import time
import glob

q = Queue.Queue(0)
mylock = threading.Lock()


class MyThread(threading.Thread):
    def __init__(self, input, worktype, tgz):
        self._jobq = input
        self._work_type = worktype
        self.tgz = tgz
        threading.Thread.__init__(self)

    def run(self):
        while True:
            if self._jobq.qsize() > 0:
                self._process_job(self._jobq.get(), self._work_type, self.tgz)
            else:
                break

    def _process_job(self, job, worktype, tgz):
        running(job, worktype, tgz)


def running(job, worktype, tgz):
    fails = None
    dti = 'None'
    serial_number = None
    sn = re.findall(CONFIG['sn_read']['read_rule'], job)
    path = os.path.dirname(job)
    txt = glob.glob(path + '/*.txt')
    if len(txt) > 0:
        with open(txt[0]) as f:
            for line in f:
                if CONFIG['report_dti_rule'] in line:
                    dti = line.replace('\n', '')
    if len(sn) > 0:
        serial_number = sn[0]
    print "Doning [%s] -- Thread (%s) " % (serial_number, worktype)
    if tgz is False:
        csv_path = job
    else:
        name = os.path.basename(job)
        a, b = shell(CONFIG['test_logs']['cmd'] % (path, name))
        csv_path = '/'.join([path, name.replace(CONFIG['test_logs']['format'], ''),
                             'bridgeOS/private/var/logs/Earthbound/Earthbound/failures.csv'])
    mylock.acquire()
    fails = read_csv(csv_path, CONFIG['csv_read']['read_key'])
    write_result(serial_number, fails, dti, result_file)
    if tgz is True:
        os.system('rm -rf %s' % os.path.join(path, name.replace(CONFIG['test_logs']['format'], '')))
    mylock.release()


def write_result(sn, list_, dti, result_file):
    if not os.path.isfile(result_file):
        dict_info = {}
        dict_two = OrderedDict()
        dict_info[dti] = dict_two
        for i in range(len(list_)):
            number = str(int(i) + 1)
            failure = list_[i]
            times = 1
            units = [sn]
            dict_two[number] = {'failure': failure,
                                'times': times,
                                'units': units}
        plistlib.writePlist(dict_info, result_file)

    else:
        dict_info = OrderedDict(plistlib.readPlist(result_file))
        new_dti = True
        for i in dict_info.keys():
            if dti == i:
                new_dti = False
                break
        if new_dti is False:
            _list_ = []
            keys = len(dict_info[dti])
            for d in dict_info[dti].keys():
                _list_.append(dict_info[dti][d]['failure'])
            for i in list_:
                if i in _list_:
                    for j in dict_info[dti].keys():
                        if i == dict_info[dti][j]['failure']:
                            dict_info[dti][j]['times'] += 1
                            dict_info[dti][j]['units'].append(sn)
                            dict_info[dti][j]['units'] = [x for x in set(dict_info[dti][j]['units'])]
                            dict_info[dti][j]['times'] = len(dict_info[dti][j]['units'])
                else:
                    keys += 1
                    dict_info[dti][str(keys)] = {
                        'failure': str(i),
                        'times': 1,
                        'units': [sn]
                    }
            plistlib.writePlist(dict_info, result_file)

        else:
            dict_two = OrderedDict()
            dict_info[dti] = dict_two
            for i in range(len(list_)):
                number = str(int(i) + 1)
                failure = list_[i]
                times = 1
                units = [sn]
                dict_two[number] = {'failure': failure,
                                    'times': times,
                                    'units': units}
            plistlib.writePlist(dict_info, result_file)


def main_thread(list_, dict_, dir_path, tgz):
    global CONFIG
    global BASEDIR
    global result_file

    BASEDIR = dir_path
    CONFIG = dict_
    result_file = os.path.join(BASEDIR, 'temp_result_' + time.strftime("%Y_%m_%d_%H_%M_%S") + '.plist')
    num_work = dict_['thread_max']
    print "Begin...."
    for i in list_:
        q.put(i)
    print "Job Qsize:", q.qsize()
    for x in range(num_work):
        MyThread(q, x, tgz).start()
