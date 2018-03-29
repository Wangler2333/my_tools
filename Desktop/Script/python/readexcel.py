#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time     : 2017/11/29上午8:45
# @Author   : Saseny Zhou
# @Site     : 
# @File     : read_excel.py
# @Software : PyCharm Community Edition


import xlrd


def read_xlsx(standard, station, station_column, name=None, args=None):
    list_ = []
    try:
        data = xlrd.open_workbook(standard)
        if name is None:
            table = data.sheets()[0]
        else:
            table = data.sheet_by_name(name)
        n = table.nrows
        for i in range(0, n):
            if i > 1:
                row_values = table.row_values(i)
                for e in station:
                    if e == row_values[station_column]:
                        if args is None:
                            list_.append(row_values)
                        else:
                            _list = []
                            for g in args:
                                _list.append(row_values[g])
                            list_.append(_list)
        return list_
    except TypeError as e:
        return list_


def excel_read(standard):
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


def define_excel(standard):
    list_ = []
    try:
        data = xlrd.open_workbook(standard)
        table = data.sheets()[0]
        nrows = table.nrows
        for i in xrange(0, nrows):
            row_values = table.row_values(i)
            list_.append(row_values)
        return list_
    except:
        return list_
