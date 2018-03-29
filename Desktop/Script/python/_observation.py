#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2017/11/19 下午8:14
@Author:   Saseny Zhou
'''

import time
import subprocess
import re
import os
import sys
import csv
import plistlib
import xlrd
from collections import OrderedDict
from optparse import OptionParser

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


class ForFailureRead(object):
    '''
    For J132 Product Burnin Observation report
    '''
    product_name = 'J132'

    def __init__(self, sn_mode='C02[A-Z].{8}', sn_cmd='system_profiler SPHardwareDataType'):
        self.sn = re.compile(sn_mode)
        self.cmd = sn_cmd
        # self.scp_cmd = '/usr/local/bin/eos-scp -r eos:/private/var/logs/Earthbound/failures.csv %s'
        self.scp_cmd = '/usr/local/bin/eos-scp eos:/private/var/logs/Earthbound/failures.csv %s'
        self.serialnumber = self.sn_read()
        self.final_path = os.path.join(base_dir, time.strftime('%Y_%m'), self.serialnumber)
        self.makedirs()

    def sn_read(self):
        code, result = shell(self.cmd)
        number = ''
        if code is 0:
            serial = self.sn.findall(str(result))
            if serial:
                number = serial[0]
        return number

    def makedirs(self):
        if not os.path.isdir(self.final_path):
            os.makedirs(self.final_path)

    def run(self):
        shell(self.scp_cmd % self.final_path)
        self.writetxt(self.final_path + '/dti.txt', self.dti())
        failure = '/'.join([self.final_path, 'failures.csv'])
        fails = self.read(failure)
        observation = '/'.join([os.path.join(base_dir, time.strftime('%Y_%m')), 'observation.plist'])
        self.compress(observation, fails, self.serialnumber)

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

    def writetxt(self, path, string):
        f = open(path, 'a')
        f.write(str(string))
        f.close()

    def dti(self):
        tb = re.compile(r'DTI: (.*?)<br/>')
        dti_version = 'None'
        a, obj = shell('cd %s; cat < %s' % ('/DTI\ Info/', 'release_notes.html'))
        if a == 0:
            for i in obj:
                t = tb.findall(i)
                if t:
                    dti_version = t[0]
                    break
        return dti_version

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


class AddFunction():
    def __init__(self):
        self.makedirs()

    def run(self, file_):
        failfile = file_
        fails = self.read(failfile)
        serial = os.path.basename(failfile).replace('.csv', '')
        observation = '/'.join([os.path.join(base_dir, time.strftime('%Y_%m')), 'observation.plist'])
        self.compress(observation, fails, serial)

    def read(self, path, key='PDCA Key', states='Status Code'):
        fails = []
        if os.path.isfile(path):
            f = open(path, 'r')
            reader = csv.DictReader(f)
            for i in reader:
                fails.append(str(i[key]).replace('/1', '') + ' (Exit Code: ' + i[states] + ')')
            f.close()
        fails = [x for x in set(fails)]
        return fails

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

    def makedirs(self):
        final_path = os.path.join(base_dir, time.strftime('%Y_%m'))
        if not os.path.isdir(final_path):
            os.makedirs(final_path)


class ReportObservation(object):
    def __init__(self, file_one, file_two):
        self.source = file_one
        self.standard = file_two
        self.final_result = os.path.join(os.path.dirname(sys.argv[0]),
                                         'final_report_' + time.strftime('%H_%M_%S') + '.csv')

    def run(self):
        final_report = []
        sou = self.readplist()
        fin = self.readcsv()
        if sou is None or fin is None:
            print 'File wrong! Pls check.'
            sys.exit(1)

        for i in xrange(int(len(sou))):
            exist = False
            for o in self.readtxt():
                if sou[str(int(i) + 1)]['failure'] == o:
                    exist = True
            if exist is False:
                self.writertxt(sou[str(int(i) + 1)]['failure'])
                x = 'New'
            else:
                x = ''
            final = [str(int(i) + 1), sou[str(int(i) + 1)]['failure'], sou[str(int(i) + 1)]['times'], [], x]
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

    def readplist(self):
        try:
            return plistlib.readPlist(self.source)
        except:
            return None

    def readcsv(self):
        try:
            list_ = []
            data = xlrd.open_workbook(self.standard)
            table = data.sheets()[0]
            nrows = table.nrows
            for i in xrange(0, nrows):
                if i > 0:
                    row_values = table.row_values(i)
                    wip, number, config = row_values
                    list_.append([str(wip), str(int(number)), str(config)])
            return list_
        except:
            return None

    def writecsv(self, final_report):
        writer = csv.writer(file(self.final_result, 'wb'))
        title = ['number', 'failure', 'times', 'units', 'new fail?']
        writer.writerow(title)
        for i in final_report:
            writer.writerow(i)

    def writertxt(self, error):
        txt = os.path.join(os.path.dirname(sys.argv[0]), 'olderror.txt')
        f = open(txt, 'a')
        f.write(str(error) + '\n')
        f.close()

    def readtxt(self):
        error_list = []
        txt = os.path.join(os.path.dirname(sys.argv[0]), 'olderror.txt')
        if not os.path.isfile(txt):
            self.writertxt('Error Code')
        f = open(txt, 'r')
        obj = f.readlines()
        f.close()
        for i in obj:
            error_list.append(i.replace('\n', ''))
        return error_list


@calculate()
def collect():
    t = ForFailureRead()
    t.run()


@calculate()
def report(file_one, file_two):
    if not os.path.isfile(file_one) or not os.path.isfile(file_two):
        print 'Files input was wrong!'
        sys.exit(1)
    t = ReportObservation(file_one, file_two)
    t.run()


def main():
    parser = OptionParser(usage="usage: %prog [options] arg")
    parser.add_option("-f", "--file", dest="filename", help="report data from FILENAME")
    parser.add_option("-v", "--verbose", action="store_true", dest="verbose")
    parser.add_option("-d", dest="alone")
    (options, args) = parser.parse_args()

    if options.verbose:
        print "Version 1.5"
        sys.exit(0)
    if options.filename:
        units_file = raw_input('Pls input units report file: ')
        report(options.filename, units_file)
        sys.exit(0)
    if options.alone:
        t = AddFunction()
        t.run(options.alone)
        sys.exit(0)

    collect()


if __name__ == "__main__":
    main()
