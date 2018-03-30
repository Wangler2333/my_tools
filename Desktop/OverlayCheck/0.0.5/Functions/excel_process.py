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
from Functions.shell import *


def file_process(args, temp, product):
    tgzFile = FileProcess()
    file_path = os.path.join(temp, str(args['download']['file key'] + args['download']['suffix']))
    line_list = args['product_info'][product]['line']
    station_list = args['product_info'][product]['station']
    sheet = excel_read(file_path, 1, header=False)
    try:
        if confirm_product(sheet, product):
            new_sheet = selection_row(line_list, station_list, sheet, product)
            final_dict = analysis(line_list, station_list, new_sheet)
            final_report = report(station_list, line_list, final_dict)
            table_show = dislplay_report(station_list, final_report)
            excel_write(product, temp, line_list, station_list, final_report)

            back_file = os.path.join(os.path.dirname(temp), 'backup',
                                     'Total_Product_' + time.strftime("%Y_%m_%d_%H_%M_%S") + args['download']['suffix'])
            os.system('mv \'%s\' %s' % (file_path, back_file))
            tgzFile.tgz_compress(back_file, force=True)
            return 0, table_show
        else:
            back_file = os.path.join(os.path.dirname(temp), 'backup',
                                     'Total_Product_' + time.strftime("%Y_%m_%d_%H_%M_%S") + args['download']['suffix'])
            os.system('mv \'%s\' %s' % (file_path, back_file))
            tgzFile.tgz_compress(back_file, force=True)
            return 1, None
    except:
        back_file = os.path.join(os.path.dirname(temp), 'backup',
                                 'Total_Product_' + time.strftime("%Y_%m_%d_%H_%M_%S") + args['download']['suffix'])
        os.system('mv \'%s\' %s' % (file_path, back_file))
        tgzFile.tgz_compress(back_file, force=True)
        return 1, None


def excel_read(file_, sheet, header=True):
    list_ = []
    try:
        data = xlrd.open_workbook(file_)
        table = data.sheets()[sheet]
        nrows = table.nrows
        print(data, table, nrows)
        for i in range(0, nrows):
            if header is True:
                list_.append(table.row_values(i))
            if header is False and i > 0:
                list_.append(table.row_values(i))
        return list_
    except TypeError as e:
        return list_


def selection_row(line_list, station_list, sheet, product):
    selection_line = []
    selection_station = []
    for i in sheet:
        if product == i[0]:
            for j in line_list:
                if j in i[1]:
                    selection_line.append(i)
    for k in selection_line:
        for l in station_list:
            if l in k[2]:
                selection_station.append(k)
    return selection_station


def analysis(line_list, station_list, new_sheet):
    final_dict = {}
    for i in station_list:
        final_dict[i] = {}
        for j in line_list:
            final_dict[i][j] = {}
            final_dict[i][j]['pass list'] = []
            final_dict[i][j]['fail list'] = []
            for l in new_sheet:
                if i in l[2] and j in l[1]:
                    if l[7] == l[8]:
                        final_dict[i][j]['pass list'].append(l)
                    else:
                        final_dict[i][j]['fail list'].append(l)
    return final_dict


def confirm_product(sheet, product):
    confirm = False
    try:
        for i in sheet:
            if product == i[0]:
                confirm = True
                break
        return confirm
    except:
        return confirm


def report(station_list, line_list, final_dict):
    final_report = {}
    default = "None"
    for i in station_list:
        final_report[i] = {}
        for j in line_list:

            if len(final_dict[i][j]['pass list']) > 0:
                default = final_dict[i][j]['pass list'][0][7]
            elif len(final_dict[i][j]['fail list']) > 0:
                default = final_dict[i][j]['fail list'][0][7]  # 修正当无pass station状态是 default version无法读取

            pass_number = str(len(final_dict[i][j]['pass list']))
            fail_number = str(len(final_dict[i][j]['fail list']))
            total_number = str(int(pass_number) + int(fail_number))
            fails = []
            if int(fail_number) > 0:
                for l in final_dict[i][j]['fail list']:
                    fails.append((str(l[3]).split('#')[1], l[5], l[7]))
            final_report[i][j] = {
                'pass number': pass_number,
                'fail number': fail_number,
                'total number': total_number,
                'fail list': fails,
                'default version': default
            }

    return final_report


def dislplay_report(station_list, final_report):
    display_list = []
    for i in station_list:
        pass_total = 0
        fail_total = 0
        default = None
        fail_list = []
        for j in final_report[i]:
            pass_total += int(final_report[i][j]['pass number'])
            fail_total += int(final_report[i][j]['fail number'])
            default = final_report[i][j]['default version']
            if len(final_report[i][j]['fail list']) > 0:
                for p in final_report[i][j]['fail list']:
                    result = str(j) + '_' + str(p[0]) + ' : ' + str(p[2])
                    fail_list.append(result)
        total = str(int(pass_total) + int(fail_total))
        display_list.append([i, default, str(fail_total) + 'F / ' + str(total) + 'T', fail_list])

    return display_list


def excel_write(product, temp, line_list, station_list, final_report):
    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet("Restore Report")
    row_one = "%s HWTE Station Overlay Default Version Result" % product
    row_two = "Date: %s" % time.strftime("%Y/%m/%d")
    header = ['Station Name', 'Default Overlay Version']
    header.extend(line_list)
    header.append("Issue Station Report")
    header.append("Comment")

    pattern = xlwt.Pattern()
    pattern.pattern = xlwt.Pattern.SOLID_PATTERN
    pattern.pattern_fore_colour = 22
    style = xlwt.XFStyle()
    style.pattern = pattern

    sheet.write_merge(0, 0, 0, 0 + len(header) - 1, row_one, style)
    sheet.write_merge(1, 1, 0, 0 + len(header) - 1, row_two, style)

    pattern = xlwt.Pattern()
    pattern.pattern = xlwt.Pattern.SOLID_PATTERN
    pattern.pattern_fore_colour = 70
    style = xlwt.XFStyle()
    style.pattern = pattern

    for h in range(len(header)):
        sheet.write(2, h, header[h], style)

    result_list = []
    for j in station_list:
        line_states = []
        issues = []
        default = "None"
        for l in line_list:

            fails = final_report[j][l]['fail number']
            total = int(fails) + int(final_report[j][l]['pass number'])
            default = final_report[j][l]['default version']

            if int(fails) > 0:
                for p in final_report[j][l]['fail list']:
                    de = str(l) + '_' + p[0] + ': ' + p[2]
                    issues.append(de)
            states = 'Fail %s / Total %s' % (fails, str(total))
            line_states.append(states)
        result = [j, default]
        result.extend(line_states)
        result.append(
            str(issues).replace("',", " ").replace("[", "").replace("]", "").replace("'", ""))  # 删除或者替换一些列表所带的字符
        result_list.append(result)

    count = 3

    for r in result_list:
        for e in range(len(header) - 1):
            if 'Total' in r[e]:

                if 'Fail 0' in str(r[e]):
                    if "Total 0" not in str(r[e]):
                        pattern = xlwt.Pattern()
                        pattern.pattern = xlwt.Pattern.SOLID_PATTERN
                        pattern.pattern_fore_colour = 50
                        style = xlwt.XFStyle()
                        style.pattern = pattern
                    else:
                        pattern = xlwt.Pattern()
                        pattern.pattern = xlwt.Pattern.SOLID_PATTERN
                        pattern.pattern_fore_colour = 2  # 42
                        style = xlwt.XFStyle()
                        style.pattern = pattern

                else:
                    pattern = xlwt.Pattern()
                    pattern.pattern = xlwt.Pattern.SOLID_PATTERN
                    pattern.pattern_fore_colour = 2  # 42
                    style = xlwt.XFStyle()
                    style.pattern = pattern


            else:
                pattern = xlwt.Pattern()
                pattern.pattern = xlwt.Pattern.SOLID_PATTERN
                pattern.pattern_fore_colour = 1
                style = xlwt.XFStyle()
                style.pattern = pattern

            sheet.write(count, e, str(r[e]), style)
        count += 1

    result_name = "Restore_Report_" + time.strftime("%Y_%m_%d_%H_%M_%S") + '.xls'
    workbook.save(os.path.join(os.path.dirname(temp), 'data', result_name))


def seconds_to_time(seconds):
    h = int(int(seconds) / 3600)
    m = int((int(seconds) % 3600) / 60)
    s = int((int(seconds) % 3600) % 60)
    if h < 10:
        h = "0" + str(h)
    if m < 10:
        m = "0" + str(m)
    if s < 10:
        s = "0" + str(s)
    return str(h) + ":" + str(m) + ":" + str(s)


def try_color():
    import xlwt
    workbook = xlwt.Workbook()
    worksheet = workbook.add_sheet('My Sheet')
    pattern = xlwt.Pattern()  # Create the Pattern
    pattern.pattern = xlwt.Pattern.SOLID_PATTERN  # May be: NO_PATTERN, SOLID_PATTERN, or 0x00 through 0x12
    #  pattern.pattern_fore_colour = 1
    #  May be: 8 through 63. 0 = Black, 1 = White, 2 = Red, 3 = Green, 4 = Blue, 5 = Yellow, 6 = Magenta, 7 = Cyan,
    #  16 = Maroon, 17 = Dark Green, 18 = Dark Blue, 19 = Dark Yellow , almost brown),
    #  20 = Dark Magenta, 21 = Teal, 22 = Light Gray, 23 = Dark Gray, the list goes on...
    style = xlwt.XFStyle()  # Create the Pattern
    pattern.pattern_fore_colour = 50  # 50
    style.pattern = pattern  # Add Pattern to Style
    worksheet.write(0, 0, 'Cell Contents', style)
    workbook.save('/Users/saseny/Desktop/Run_in/Excel_Workbook.xls')
