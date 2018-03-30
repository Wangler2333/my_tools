#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time     : 2018/3/15上午11:30
# @Author   : Saseny Zhou
# @Site     : 
# @File     : excel_read.py
# @Software : PyCharm


import xlrd
from Path.path import *
import csv
from shutil import copy


def excel_read(file, location=None, sheet=None, station=None):
    try:
        data = xlrd.open_workbook(file)
        if sheet is None:
            table = data.sheets()[0]
        else:
            table = data.sheet_by_name(sheet)
        n = table.nrows
        for i in range(0, n):
            tmp = table.row_values(i)
            if station is not None:
                for j in station:
                    for l in tmp:
                        if str(j) in str(l):
                            if location is not None:
                                yield tmp[location[0]], tmp[location[1]]
                            else:
                                yield tmp
            else:
                if location is not None:
                    if len(location) == 3:
                        yield tmp[location[0]], tmp[location[1]], tmp[location[2]]
                    else:
                        yield tmp[location[0]], tmp[location[1]]
                else:
                    yield tmp
    except:
        pass


def find_file(path, format):
    a = []
    try:
        fns = [os.path.join(root, fn) for root, dirs, files in os.walk(path) for fn in files]
        for f in fns:
            if os.path.isfile(f):
                if format in f:
                    a.append(f)
    except:
        pass
    return a


def file_read(file):
    return_list = []
    try:
        f = open(file, "r")
        f_obj = f.readlines()
        for i in f_obj:
            return_list.append(str(i).replace("\n", ""))
        f.close()
    except:
        pass
    return return_list


def write_csv(dict_info, path):
    """列表方式写入CSV文件"""
    try:
        csvFile = open(path, "a")
        f_write = csv.writer(csvFile)
        for i in dict_info:
            f_write.writerow(i)
        csvFile.close()
    except:
        print('Write CSV file Fail')


def copy_file(source, target):
    try:
        if not os.path.isfile(source):
            copy(source, target)
        else:
            print("[%s] file not exist." % source)
    except:
        pass


def error_code_file_to_json(configInfo):
    config = configInfo["process"]["Excel Read"]
    filePath = os.path.join(resources, config["file name"])
    location = [config["location"]["code"], config["location"]["error"]]
    error_dict = {}
    try:
        for i in excel_read(filePath, location=location, sheet=config["sheet name"], station=config["station"]):
            if i[1] and "New Failure" not in i[1]:
                if error_dict.get(str(i[1]), False) is False:
                    error_dict[str(i[1])] = str(int(i[0]))
                    collectionData.logger.info("Read Error Code File: {}".format({str(i[1]): str(int(i[0]))}))
    except:
        pass
    write_json_file(error_dict, errorJsonPath)


def unit_number_file_to_json(configInfo):
    config = configInfo["process"]["Unit Number"]
    filePath = os.path.join(resources, config["file name"])
    location = [config["location"]["serial number"], config["location"]["unit number"],
                config["location"]["config info"]]
    snRule = configInfo["process"]["Serial Number"]["read rule"]
    unit_dict = {}
    try:
        for i in excel_read(filePath, location=location, sheet=config["sheet name"]):
            serial_number = re.findall(snRule, str(i[0]))
            if serial_number:
                if unit_dict.get(serial_number[0], False) is False:
                    unit_dict[serial_number[0]] = {
                        "wip": str(i[0]),
                        "number": str(int(i[1])),
                        "config": str(i[2])
                    }
                    collectionData.logger.info("Read Units File: {}".format({serial_number[0]: {
                        "wip": str(i[0]),
                        "number": str(int(i[1])),
                        "config": str(i[2])
                    }}))
    except:
        pass
    write_json_file(unit_dict, unitJsonPath)


def read_error_message_to_json(file):
    if os.path.isfile(errorMessageJsonPath):
        failuresDict = read_json_file(errorMessageJsonPath)
        if failuresDict is False:
            failuresDict = {}
    else:
        failuresDict = {}
    print(failuresDict)
    try:
        readInfo = excel_read(file, sheet="Defects", location=[2, 5, 8])
        for i in readInfo:
            if re.findall(r'C02[A-Z].{8}', str(i[0])):
                if failuresDict.get(str(i[0]), False) is False:
                    failuresDict[str(i[0])] = [str(i[1])]
                    collectionData.logger.info({str(i[0]): str(i[1])})
                else:
                    tmp = failuresDict[str(i[0])]
                    if str(i[1]) not in tmp:
                        tmp.append(str(i[1]))
                        collectionData.logger.info({str(i[0]): str(i[1])})
    except:
        pass
    write_json_file(failuresDict, errorMessageJsonPath)
