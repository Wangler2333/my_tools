#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time     : 2017/11/18下午6:10
# @Author   : Saseny Zhou
# @Site     : 
# @File     : observation.py
# @Software : PyCharm Community Edition

import time
import subprocess
import sys
import os
import re
import csv
import plistlib

index = {
    'number': {
        'failure': '',
        'times': '',
        'units': []
    }
}

scp_cmd = '/usr/local/bin/eos-scp -r eos:/private/var/logs/Earthbound/failures.csv %s'


def shell(cmd):
    try:
        run = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        while run.poll() is None:
            pass
        return_code = run.returncode
        return_list = [str(x).replace('\n', '') for x in run.stdout.readlines()]
        return return_code, return_list
    except IOError as e:
        print 'IOError ', e


def calculate(flag=False):
    def showtime(func):
        def inner(*args, **kwargs):
            strt_time = time.time()
            func(*args, **kwargs)
            end_time = time.time()
            print('Used Time: %s s' % (round(float(end_time) - float(strt_time), 2)))
            if flag:
                pass

        return inner

    return showtime


def serial_number():
    sn = re.compile('C02[A-Z].{8}')
    code, result = shell('system_profiler SPHardwareDataType')
    number = 'None'
    if code is 0:
        serial = sn.findall(str(result))
        if serial:
            number = serial[0]
    return number


def readcsv(path, key='PDCA Key'):
    fails = []
    if os.path.isfile(path):
        f = open(path, 'r')
        reader = csv.DictReader(f)
        for i in reader:
            fails.append(i[key])
        f.close()
    fails = [x for x in set(fails)]
    return fails


def compress(result, fails, sn):
    if not os.path.isfile(result):
        dict_info = {}
        for i in range(len(fails)):
            number = str(int(i) + 1)
            failure = fails[i]
            times = 1
            units = [sn]
            dict_info[number] = {'failure': failure,
                                 'times': times,
                                 'units': units}
        plistlib.writePlist(dict_info, result)
    else:
        dict_info = plistlib.readPlist(result)
        list_ = []
        keys = len(dict_info)
        for d in dict_info.keys():
            list_.append(dict_info[d]['failure'])
        for i in fails:
            if i in list_:
                for j in dict_info.keys():
                    if i == dict_info[j]['failure']:
                        dict_info[j]['times'] += 1
                        dict_info[j]['units'].append(sn)
            else:
                keys += 1
                dict_info[str(keys)] = {
                    'failure': str(i),
                    'times': 1,
                    'units': [sn]
                }
        plistlib.writePlist(dict_info, result)


@calculate()
def process():
    dir_path = '/'.join([os.path.dirname(sys.argv[0]), time.strftime('%Y_%m_%d')])
    serial = serial_number()
    if not os.path.isdir(os.path.join(dir_path, serial)):
        os.makedirs(os.path.join(dir_path, serial))
    shell(scp_cmd % os.path.join(dir_path, serial))
    failfile = '/'.join([os.path.join(dir_path, serial), 'failures.csv'])
    faillist = readcsv(failfile)
    observation = '/'.join([dir_path, 'observation.plist'])
    compress(observation, faillist, serial)


process()
