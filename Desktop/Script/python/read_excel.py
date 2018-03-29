#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time     : 2017/11/14下午12:25
# @Author   : Saseny Zhou
# @Site     : 
# @File     : read_excel.py
# @Software : PyCharm Community Edition


import xlrd
import time


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


class ExcelRead(object):
    def __init__(self, file, station, scope, sheet, un_expect):
        self.file = file
        self.station = station
        self.scope = scope
        self.sheet = sheet
        self.un_expect = un_expect
        self.number, self.list = self.selection()

    def read(self):
        sh = None
        try:
            dk = xlrd.open_workbook(self.file)
            sh = dk.sheet_by_name(self.sheet)
        except NameError and FileNotFoundError as e:
            print('Error Found was', e)
        return sh

    def selection(self):
        f_obj = self.read()
        error_dict = {}
        if f_obj:
            for i in range(1, f_obj.nrows):
                row_data = f_obj.row_values(i)
                for j in self.station:
                    if j == row_data[int(self.scope[0]) + 1] and self.un_expect % j not in row_data:
                        number, station, message = row_data[self.scope[0]:self.scope[1]]
                        error_dict[str(int(number))] = {station: message}
        return len(error_dict), error_dict

    def search(self, info):
        result = {}
        return_list = []
        a = self.list
        if info in a.keys():
            result[info] = a[info]
            return_list.append(result)
        result = {}
        for i in a.keys():
            for j in a[i].values():
                if str(info).upper() in str(j).upper():
                    result[i] = a[i]
                    return_list.append(result)
        return_list = [x for x in return_list]
        return len(return_list), return_list


t = ExcelRead(file='/Users/saseny/Desktop/ERROR.xlsx', scope=(2, 5),
              station=['Log collection', 'Run-in', 'Shipping_Settings'],
              sheet='Error Codes', un_expect='[New Failure] %s')


@calculate()
def running(info):
    print('You choosed station has %s error code.' % t.number)
    print(t.search(info))


running('kp')
