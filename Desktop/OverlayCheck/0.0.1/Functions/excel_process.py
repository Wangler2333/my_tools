#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time     : 2017/12/9上午9:38
# @Author   : Saseny Zhou
# @Site     : 
# @File     : excel_process.py
# @Software : PyCharm Community Edition

import os
import xlrd
import time
import xlwt


def file_process(args, temp, product):
    try:
        file_path = os.path.join(temp, str(args['download']['file key'] + args['download']['suffix']))
        sheet1 = excel_read(file_path, 0, header=False)
        sheet2 = excel_read(file_path, 1, header=False)
        line_list = args['product_info'][product]

        new_sheet1 = eliminate(sheet1, product, line_keys=line_list)
        station_list = station(new_sheet1)

        pass_, fails_ = analysis(station_list, new_sheet1)
        fails_result = search_info(fails_, sheet2)

        report_list = report(pass_, fails_result)

        os.system('mv \'%s\' %s' % (
            file_path, os.path.join(os.path.dirname(temp), 'backup',
                                    time.strftime("%Y_%m_%d_%H_%M_%S") + args['download']['suffix'])))
        return 0, report_list
    except:
        return 1, None


def excel_read(file_, sheet, header=True):
    list_ = []
    try:
        data = xlrd.open_workbook(file_)
        table = data.sheets()[sheet]
        nrows = table.nrows
        for i in range(0, nrows):
            if header is True:
                list_.append(table.row_values(i))
            if header is False and i > 0:
                list_.append(table.row_values(i))
        return list_
    except IOError as e:
        return list_


def overlay_check(args, default, current):
    for i in args:
        if i[default] != i[current]:
            yield i


def eliminate(source, product, line_keys=None, station_keys=None):
    return_list = []
    for i in source:
        if i[0] == product:
            if line_keys is None and station_keys is None:
                return_list.append(i)
            if line_keys is not None and station_keys is None:
                for j in line_keys:
                    if j in i[1]:
                        return_list.append(i)
            if line_keys is None and station_keys is not None:
                for j in station_keys:
                    if j in i[2]:
                        return_list.append(i)
            if line_keys is not None and station_keys is not None:
                for j in line_keys:
                    for l in station_keys:
                        if j in [1] and l in i[2]:
                            return_list.append(i)
    return return_list


def search_info(one, two):
    for i in one.keys():
        files = []
        for j in one[i]['fail list']:
            for l in two:
                if j[1] == l[1] and j[2] == l[2] and j[4] == l[7]:
                    files.append(l)
                    time.sleep(1)

        one[i]['fail list'] = files
    return one


def station(args):
    station_list = []
    for i in args:
        station_list.append(i[2])
    return [x for x in set(station_list)]


def analysis(station_list, new_sheet):
    pass_dict = {}
    fail_dict = {}
    for i in new_sheet:
        for j in station_list:
            if j == i[2]:

                if i[3] == i[4]:
                    if j not in pass_dict.keys():
                        pass_dict[j] = {
                            'times': 1,
                            'pass list': [i, ]
                        }
                    else:
                        pass_dict[j]['times'] += 1
                        pass_dict[j]['pass list'].append(i)
                else:
                    if j not in fail_dict.keys():
                        fail_dict[j] = {
                            'times': 1,
                            'fail list': [i, ]
                        }
                    else:
                        fail_dict[j]['times'] += 1
                        fail_dict[j]['fail list'].append(i)
    return pass_dict, fail_dict


def report(pass_dict, fail_dict):
    final_result = {}
    for i in pass_dict:
        final_result[i] = {
            'default overlay': pass_dict[i]['pass list'][0][3],
            'pass times': pass_dict[i]['times'],
            'fail report': [],
            'fail times': 0
        }
        for j in fail_dict:
            if i == j:
                final_result[i]['fail times'] = fail_dict[j]['times']
                for l in fail_dict[j]['fail list']:
                    po = l[5], l[7]
                    final_result[i]['fail report'].append(po)
    return final_result

# from Config.config import *
#
# for i in file_process(read_json_file('/Volumes/DEVELOPMENT/App_Design/Check/Resources/config.json'),
#                       '/Volumes/DEVELOPMENT/App_Design/Check/Resources/tmp', 'J79A'):
#     print(i)
