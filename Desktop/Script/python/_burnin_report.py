#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time     : 2017/11/20上午9:39
# @Author   : Saseny Zhou
# @Site     : 
# @File     : _burnin_report.py
# @Software : PyCharm Community Edition


import os
import sys
import subprocess
import time
import re
import plistlib
from optparse import OptionParser
import xlrd
import csv

base_dir = os.path.dirname(sys.argv[0])

PATH = {
    'release_notes': '/DTI\ Info/',
    'default_summary': {
        'default': False,
        'path': '/Users/saseny/Desktop/J132/_tools/'
    },
    'special_index': 'PDCA Key',
    'dti': 'DTI: (.*?)<br/>',
    'sn': 'C02[A-Z].{8}',
    'cmd': 'system_profiler SPHardwareDataType',
    'station': ['Run-in', 'Log collection']
}


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


def plist(default):
    if not os.path.isfile(default):
        plistlib.writePlist(PATH, default)
    return plistlib.readPlist(default)


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


class BurninReport(object):
    def __init__(self, default):
        self.dict = default
        self.sn = re.compile(self.dict['sn'])
        self.tb = re.compile(self.dict['dti'])
        self.cmd = self.dict['cmd']
        self.serial_number = self.sn_read()

        if self.dict['default_summary']['default'] is False:
            self.target_path = os.path.join(base_dir, self.serial_number)
        else:
            self.target_path = os.path.join(self.dict['default_summary']['path'], self.serial_number)
        self.makesdir()

        # self.scp_cmd = '/usr/local/bin/eos-scp -r eos:/private/var/logs/Earthbound/failures.csv %s'
        self.scp_cmd = '/usr/local/bin/eos-scp eos:/private/var/logs/Earthbound/failures.csv %s'

    def sn_read(self):
        code, result = shell(self.cmd)
        number = ''
        if code is 0:
            serial = self.sn.findall(str(result))
            if serial:
                number = serial[0]
        return number

    def dti(self):
        dti_version = 'None'
        a, obj = shell('cd %s; cat < %s' % (self.dict['release_notes'], 'release_notes.html'))
        if a == 0:
            for i in obj:
                t = self.tb.findall(i)
                if t:
                    dti_version = t[0]
                    break
        return dti_version

    def openfile(self):
        if os.path.isfile(self.dict['release_notes']):
            f = open(self.dict['release_notes'], 'r')
            f_obj = f.readlines()
            f.close()
            return f_obj
        else:
            return False

    def makesdir(self):
        if not os.path.isdir(self.target_path):
            os.makedirs(self.target_path)

    def run(self, error_code=None):
        dti_version = self.dti()
        shell(self.scp_cmd % self.target_path)
        fail_file = '/'.join([self.target_path, 'failures.csv'])
        self.compress(fail_file, error_code, dti_version)

    def compress(self, fail_file, error_code, dti_version):
        fials = self.read(fail_file)
        codes = self.readxlsx(error_code)

        have = []
        not_yet = []

        for i in fials:
            done = False
            for j in codes:
                if i == j[2]:
                    done = True
                    have.append(j[1])
            if done is False:
                not_yet.append(i)

        print '机器序列号:', self.serial_number
        print 'DTI 版本:', dti_version.split('_')[1]
        print 'Error Code:', have
        print '需增加:', not_yet

        for d in [self.serial_number, dti_version, have, not_yet]:
            self.writefile(d)

    def read(self, path, key='PDCA Key', code='Status Code'):
        fails = []
        if os.path.isfile(path):
            f = open(path, 'r')
            reader = csv.DictReader(f)
            for i in reader:
                fails.append(i[key] + ' (Exit code: ' + i[code] + ')')
            f.close()
        fails = [x for x in set(fails)]
        return fails

    def readxlsx(self, error):
        list_ = []
        data = xlrd.open_workbook(error)
        table = data.sheet_by_name('Error Codes')
        nrows = table.nrows
        for i in xrange(0, nrows):
            if i > 0:
                row_values = table.row_values(i)
                for j in self.dict['station']:
                    if j == row_values[3]:
                        if '[New Failure] %s' % j != row_values[4]:
                            message, number, station = row_values[4], row_values[2], row_values[3]
                            list_.append([station, str(int(number)), message])
        return list_

    def writefile(self, sting):
        txt = os.path.join(self.target_path, 'result.txt')
        f = open(txt, 'a')
        f.write(str(sting) + '\n')
        f.close()


@calculate()
def main():
    parser = OptionParser(usage="usage: %prog [options] arg")
    parser.add_option("-f", "--file", dest="filename", help="report data from FILENAME")
    parser.add_option("-z", dest="csvfile", help="report data from FILENAME")
    parser.add_option("-v", "--verbose", action="store_true", dest="verbose")
    (options, args) = parser.parse_args()
    if options.verbose:
        print "Version 1.2"
        sys.exit(0)
    if options.filename:
        default = plist(os.path.join(base_dir, 'default.plist'))
        t = BurninReport(default)
        t.run(options.filename)
        sys.exit(0)
    if options.csvfile:
        default = plist(os.path.join(base_dir, 'default.plist'))
        files = options.csvfile
        error = os.path.join(base_dir, 'ERROR.xlsx')
        if not os.path.isfile(error):
            print 'ERROR.xlsx not exist!'
            sys.exit(1)
        t = BurninReport(default)
        t.compress(files, error, '_Unknown_')


if __name__ == "__main__":
    main()
