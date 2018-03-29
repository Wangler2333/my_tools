#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time     : 2017/11/24下午1:50
# @Author   : Saseny Zhou
# @Site     : 
# @File     : report.py
# @Software : PyCharm Community Edition


import sys
import os
import re
import csv
from collections import OrderedDict
import plistlib
import xlrd
import time
from optparse import OptionParser
import subprocess
import threading
import Queue

base_dir = os.path.dirname(sys.argv[0])


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


class Report(object):
    def __init__(self, path, format, stand=None):
        self.path = path
        self.formt = format
        self.tb = re.compile('C02[A-Z].{8}')
        self.final_result = os.path.join(os.path.dirname(sys.argv[0]), 'result.csv')
        self.stand = stand

    def read(self, path, key='PDCA Key', states='Status Code'):
        fails = []
        if os.path.isfile(path):
            f = open(path, 'r')
            reader = csv.DictReader(f)
            for i in reader:
                fails.append(str(i[key]).replace('/1', '') + ' (Exit code: ' + i[states] + ')')
            f.close()
        fails = [x for x in set(fails)]
        return fails

    def find_file(self):
        try:
            find_list = []
            fns = [os.path.join(root, fn) for root, dirs, files in os.walk(self.path) for fn in files]
            for f in fns:
                if os.path.isfile(f):
                    if self.formt in f:
                        find_list.append(f)
            return find_list
        except IOError as o:
            print('IOError', o)

    def find_sn(self, name):
        sn = self.tb.findall(name)
        if len(sn) > 0:
            return sn[0]
        else:
            return None

    @calculate()
    def running(self):
        observation = '/'.join([base_dir, 'observation.plist'])

        file_list = self.find_file()
        for i in file_list:
            tinue_ = False
            serial_number = self.find_sn(i)
            print 'Doing unit [%s]' % serial_number

            if tgz is True:
                road = self.un_tgz(i)
                if road is False:
                    tinue_ = False
                if tinue_ is True:
                    fails = self.read(road)
                shell('rm -rf %s' % str(i).replace('.tgz', ''))
            else:
                tinue_ = True
                fails = self.read(i)

            if tinue_ is True:
                self.compress(observation, fails, serial_number)

        self.run(observation, self.stand)

    def compress(self, result, fails, sn):
        if not os.path.isfile(result):
            dict_info = OrderedDict()
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
            dict_info = OrderedDict(plistlib.readPlist(result))
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

    def readplist(self, source):
        try:
            return plistlib.readPlist(source)
        except:
            return None

    def readxlsx(self, standard):
        list_ = []
        try:
            data = xlrd.open_workbook(standard)
            table = data.sheets()[0]
            nrows = table.nrows
            for i in xrange(0, nrows):
                if i > 0:
                    row_values = table.row_values(i)
                    wip, number, config = row_values
                    list_.append([str(wip), str(int(number)), str(config)])
            return list_
        except:
            return list_

    def writecsv(self, final_report):
        writer = csv.writer(file(self.final_result, 'wb'))
        title = ['number', 'failure', 'times', 'units']
        writer.writerow(title)
        for i in final_report:
            writer.writerow(i)

    def run(self, source, standard):
        final_report = []
        sou = self.readplist(source)
        fin = self.readxlsx(standard)
        if sou is None or fin is None:
            print 'File wrong! Pls check.'
            sys.exit(1)

        for i in xrange(int(len(sou))):
            final = [str(int(i) + 1), sou[str(int(i) + 1)]['failure'], sou[str(int(i) + 1)]['times'], []]
            for j in sou[str(int(i) + 1)]['units']:
                write = False
                for l in fin:
                    if j in l[0]:
                        write = True
                        final[3].append('#' + str(l[1]))
                if write is False:
                    final[3].append(j)
            final_report.append(final)
        self.writecsv(final_report)

    def un_tgz(self, file_):
        path = os.path.dirname(file_)
        name = os.path.basename(file_)
        a, b = shell('cd %s; tar -zxf %s' % (path, name))
        if a != 0:
            print 'tgz wrong file.'
            return False

        csv_path = '/'.join([path, name.replace('.tgz', ''),
                             'bridgeOS/private/var/logs/Earthbound/Earthbound/failures.csv'])
        if not os.path.isfile(csv_path):
            print 'No failures.csv exist.'
            return False
        return csv_path


def main():
    global tgz
    tgz = False
    parser = OptionParser(usage="usage: %prog [options] arg")
    parser.add_option("-p", "--path", dest="PathRoad", help="input failure.csv files folder")
    parser.add_option("-t", "--tgz", dest="tgzPath", help="input tgz fail logs folder")
    parser.add_option("-n", dest="roadPath",
                      help="input failure.csv files folder, then input excel file with units info")
    parser.add_option("-g", dest="tzgRoad",
                      help="input tgz fail logs folder, then input excel file with units info")
    parser.add_option("-v", "--verbose", action="store_true", dest="verbose")
    (options, args) = parser.parse_args()

    if options.PathRoad:
        t = Report(options.PathRoad, '.csv')
        t.running()
        sys.exit(0)

    if options.tgzPath:
        tgz = True
        t = Report(options.tgzPath, '.tgz')
        t.running()
        sys.exit(0)

    if options.roadPath:
        units_file = raw_input('请输入units_number文件: ')
        if not os.path.isfile(units_file) or '.xlsx' not in units_file:
            print 'units_number file was wrong.'
            sys.exit(1)
        t = Report(options.roadPath, '.csv', stand=units_file)
        t.running()
        sys.exit(0)

    if options.tzgRoad:
        tgz = True
        units_file = raw_input('请输入units_number文件: ')
        if not os.path.isfile(units_file) or '.xlsx' not in units_file:
            print 'units_number file was wrong.'
            sys.exit(1)
        t = Report(options.tzgRoad, '.tgz', stand=units_file)
        t.running()
        sys.exit(0)

    if options.verbose:
        print 'Version: 1.0'
        sys.exit(0)


if __name__ == "__main__":
    main()
