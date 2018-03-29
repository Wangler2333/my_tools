#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import glob
import csv
import sys
import re


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


def Force_Actuatorcal(files, result, sn):
    for file in files:
        CSV = []
        CSV_ = []

        CSV_.append(sn)
        csvfile = open(file, 'rb')
        cs = csv.reader(csvfile)
        for line in cs:
            CSV.append(line)

        if not os.path.isfile(result):
            CSVe = ['Serial Number']
            cd = CSVe + CSV[0]
            writer = csv.writer(open(result, 'a'))
            writer.writerow(cd)

        cv = CSV_ + CSV[-1]
        writer = csv.writer(open(result, 'a'))
        writer.writerow(cv)
        csvfile.close()


def doJob(logs):
    for log in logs:
        FirstName = re.findall(r'C02.{9}', log)
        print FirstName
        filepath = os.path.dirname(log)
        os.system('cd %s ; tar -zxf %s &>/dev/null' % (filepath, log))
        FolderName = str(log).replace('.tgz', '')

        if "PASS" in log:
            ActuatorCal_File = glob.glob(FolderName + '/*/ActuatorCal_Summary/*')
            Froce_File = glob.glob(FolderName + '/*/ForceCal_Summary/*')

        if "FAIL" in log:
            ActuatorCal_File = glob.glob(FolderName + '/*/Logs/ActuatorCal_Summary/*')
            Froce_File = glob.glob(FolderName + '/*/Logs/ForceCal_Summary/*')

        if len(Froce_File) > 0:
            Force_Actuatorcal(Froce_File, Force_Result, FirstName[0])
        if len(ActuatorCal_File) > 0:
            Force_Actuatorcal(ActuatorCal_File, Actuatorcal_Result, FirstName[0])

        os.system('rm -rf %s' % FolderName)


if __name__ == '__main__':
    Default_Path = raw_input("请输入Logs路径:")
    Force_Result = os.path.dirname(sys.argv[0]) + '/Force_Result.csv'
    Actuatorcal_Result = os.path.dirname(sys.argv[0]) + '/Actuatorcal_Result.csv'

    doJob(find_file(Default_Path, '.tgz'))
