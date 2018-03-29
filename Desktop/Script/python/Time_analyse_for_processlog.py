#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Create by Saseny on 2017/07/01

import sys
import plistlib
import threading
import Queue
import os
import re
import glob
import time
import csv
import matplotlib
import pandas

print "\033[1;32m" + '''
输出文件在脚本同目录下 result_for_check 文件夹下:

 -  1 Table_left_time.csv 所有测试tab时间;
 -  2 Item_left_time.csv 所有测试项目时间，由于用的是列表存储数值，所以会存在bug;
 -  3 Command_left_time.csv 所有测试command时间，bug同上;
 -  4 待增加： 选择code or set 进行所有同code or set数值生成曲线图.

 -- 输入'1',进入标准参数设定，需输入标准processlog用于存储标准，item,command数值并用于后续计算仅打印pipei标准参数的值;
    若不输入则会以第一个处理的log进行标准取值(建议选择标准log).         

-->> 设 置： 跳过CQA Log, 以及跳过有(Fail)或者(Retry)的Log,
     注 意： 拖入log路径之后请删除路径最后的空格, Log 压缩文件必须以(.tgz)结尾.

''' + "\033[0m"

q = Queue.Queue(0)
NUM_WORKERS = 10
mylock = threading.Lock()

os.system('mkdir -p %s' % os.path.dirname((sys.argv[0])) + '/Result/')
os.system('rm -rf %s' % os.path.dirname((sys.argv[0])) + '/Result/*')

config_test_item_path = os.path.dirname(sys.argv[0]) + '/Config/' + 'item_Expected.plist'
config_command_item_path = os.path.dirname(sys.argv[0]) + '/Config/' + 'command_Expected.plist'
result_test_item_path = os.path.dirname(sys.argv[0]) + '/Result/' + 'TestItemTime.csv'
result_command_item_path = os.path.dirname(sys.argv[0]) + '/Result/' + 'TestCommandTime.csv'
result_main_item_path = os.path.dirname(sys.argv[0]) + '/Result/' + 'TestMainTime.csv'


class MyThread(threading.Thread):
    def __init__(self, input, worktype):
        self._jobq = input
        self._work_type = worktype
        threading.Thread.__init__(self)

    def run(self):
        while True:
            if self._jobq.qsize() > 0:
                self._process_job(self._jobq.get(), self._work_type)
            else:
                break

    def _process_job(self, job, worktype):
        doJob(job, worktype)


def writefile(string, file):
    try:
        with open(file, 'a') as d:
            d.write(string + '\n')
    except IOError as i:
        print ('IOError:', i)


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


def Time_chek(_time):
    try:
        timeArray = time.strptime(_time, "%Y/%m/%d %H:%M:%S")
        timeStamp = int(time.mktime(timeArray))
        return timeStamp
    except UnboundLocalError as p:
        print ('UnboundLocalError', p)


def time_add(time1, time2):
    time_s_1 = str(time1).split('m')[1].split('s')[0]
    time_s_2 = str(time2).split('m')[1].split('s')[0]
    time_m_1 = str(time1).split('h')[1].split('m')[0]
    time_m_2 = str(time2).split('h')[1].split('m')[0]
    time_h_1 = str(time1).split('h')[0]
    time_h_2 = str(time2).split('h')[0]
    s_time = int(time_s_1) + int(time_s_2)
    dd = 0
    ee = 0
    if s_time > 60:
        dd = s_time % 60
    m_time = int(time_m_1) + int(time_m_2) + int(dd)
    if m_time > 60:
        ee = m_time % 60
    h_time = int(time_h_1) + int(time_h_2) + ee
    Startup_time = str(h_time) + 'h' + str(m_time) + 'm' + str(s_time) + 's'
    return Startup_time


def Time_calculate(Start, End):
    '''
    d = int(End) - int(Start)
    hour = d / 3600
    d1 = d % 3600
    min = d1 / 60
    d2 = d1 % 60
    time = str(hour) + "h" + str(min) + "m" + str(d2) + "s"
    return time
    '''  # -- >>
    return int(End) - int(Start)


def doJob(job, worktype):
    file_path = str(job)
    filepath = os.path.dirname(file_path)
    log_folder_name = file_path.replace('.tgz', '')
    Running = False
    SerialNumber = ""
    processlog_path = ""

    os.system('cd %s ; tar -zxf %s &>/dev/null' % (filepath, file_path))

    serial_number = re.findall(r'C02[A-Z]\w{8}', log_folder_name)

    if len(serial_number) > 0:
        SerialNumber = serial_number[0]

    pass_log_path = glob.glob(log_folder_name + '/*/processlog.plog')
    fail_log_path = glob.glob(log_folder_name + '/*/*/processlog.plog')

    if len(pass_log_path) > 0:
        processlog_path = pass_log_path[0]
        Running = True
    if len(fail_log_path) > 0:
        processlog_path = fail_log_path[0]
        Running = True
    if "CQA" in processlog_path:
        Running = False

    if Running == True:

        print "Doing -- [" + str(SerialNumber) + "]" \
                                                 " --- Thread@ " + str(worktype) + " Start"
        mylock.acquire()
        Processing(processlog_path, SerialNumber, log_folder_name)
        print "Done  -- [" + str(SerialNumber) + "]" \
                                                 " --- Thread@ " + str(worktype) + " End"
        os.system('rm -rf %s' % log_folder_name)

        mylock.release()
    else:
        print "\033[0;31m" + "doing", log_folder_name, "" \
                                                       " --- worktype Log Was Wrong -Thread@ ", str(
            worktype) + "\033[0m"
        os.system('rm -rf %s' % log_folder_name)


def item_check(file, filename):
    '''

    :param file: file for test item config colloct (processlog.plog);
    :param filename: the result path (item_Expected.plist);
    :return: no return value and only return plist file with all test item info.

    '''

    item = {}
    n = 0

    with open(file) as f:
        for line in f:
            if "TEST-TSTT" in line:

                code = re.findall(r'tid="([0-9]*)"', line)
                name = re.findall(r'tname="(.*?)"', line)
                formt = re.findall(r'sid="(.*?)"', line)

                if len(code) > 0 and len(name) > 0 and len(formt) > 0:
                    n = n + 1
                    test_item = {
                        "item": str(formt[0]),
                        "code": str(code[0]),
                        "info": str(name[0])
                    }
                    item[str(n)] = test_item
    plistlib.writePlist(item, filename)


def command_check(file, filename):
    '''

    :param file: file for test command config colloct (processlog.plog);
    :param filename: the result path (command_Expected.plist);
    :return: no return value and only return plist file with all command item info.

    '''

    command = {}
    n = 0
    a = 0
    b = 0

    with open(file) as f:
        for line in f:

            if "CMMD-CSTT" in line and "action.command" not in line:

                name = re.findall(r'ProcessName="(.*?)"', line)
                command_line = re.findall(r'CommandLine="(.*?)"', line)
                location = re.findall(r'TableName="(.*?)"', line)
                message = re.findall(r'Message="(.*?)"', line)

                if len(name) > 0 and len(command_line) > 0 and len(location) > 0:
                    n = n + 1
                    command_item = {
                        "name": str(name[0]),
                        "line": str(command_line[0]),
                        "location": str(location[0])
                    }
                    command[str(n)] = command_item

                if len(name) > 0 and len(message) > 0 and len(location) > 0:
                    n = n + 1
                    command_item = {
                        "name": str(name[0]),
                        "message": str(message[0]),
                        "location": str(location[0])
                    }
                    command[str(n)] = command_item

            if "CMMD-CRST" in line and "action.command" not in line:

                name = re.findall(r'ProcessName="(.*?)"', line)
                command_line = re.findall(r'CommandLine="(.*?)"', line)
                location = re.findall(r'TableName="(.*?)"', line)
                message = re.findall(r'Message="(.*?)"', line)

                if len(name) > 0 and len(command_line) > 0 and len(location) > 0:
                    n = n + 1
                    command_item = {
                        "name": str(name[0]),
                        "line": str(command_line[0]),
                        "location": str(location[0])
                    }
                    command[str(n)] = command_item

                if len(name) > 0 and len(message) > 0 and len(location) > 0:
                    n = n + 1
                    command_item = {
                        "name": str(name[0]),
                        "message": str(message[0]),
                        "location": str(location[0])
                    }
                    command[str(n)] = command_item
    del command[str(len(command.keys()))]  #
    j = 1
    for i in range(int(len(command.keys())) / 2):
        if str(command[str(j)]) == str(command[str(j + 1)]):
            a = 1
        if str(command[str(j)]) != str(command[str(j + 1)]):
            b = 1
        j = j + 2

    if a == 1 and b != 1:
        plistlib.writePlist(command, filename)


def export_config_file(file):
    os.system('mkdir -p %s' % os.path.dirname((sys.argv[0])) + '/Config/')
    os.system('rm -rf %s' % os.path.dirname((sys.argv[0])) + '/Config/*')
    item_check(file, config_test_item_path)
    command_check(file, config_command_item_path)
    os.system('cp -rf %s %s' % (file, os.path.dirname((sys.argv[0])) + '/Config/'))


def check_config_file(file):
    if not os.path.isfile(config_test_item_path):
        export_config_file(file)
    if not os.path.isfile(config_command_item_path):
        export_config_file(file)


def read_config(path):
    try:
        Storage = "None"
        Processor = "None"
        Memorry = "None"
        Keyboard = "None"
        with open(path) as f:
            for line in f:
                if Storage == "None":
                    ssd = re.findall(r'devicecapacity = "(.*?)"', line)
                    if len(ssd) > 0:
                        Storage = str(ssd[0]) + "GB"
                if Processor == "None":
                    cpu = re.findall(r'frequency = "(.*?)"', line)
                    if len(cpu) > 0:
                        Processor = str(float(float(cpu[0]) / 1000)) + "GHz"
                if Memorry == "None":
                    memory = re.findall(r'size = "(.*?)" & type = "Memory"', line)
                    if len(memory) > 0:
                        Memorry = str(memory[0]) + "GB"
                if Keyboard == "None":
                    keyboard = re.findall(r'identifier = "Apple Internal Keyboard / Trackpad" & language = "(.*?)"',
                                          line)
                    if len(keyboard) > 0:
                        Keyboard = str(keyboard[0])
        return str(Storage), str(Processor), str(Memorry), str(Keyboard)
    except IOError as e:
        print ('IOError', e)


def Processing(filename, serialnumber, FileName):
    check_config_file(filename)
    memorry_vendor = "None"
    Bundle = "None"
    fail_state = 0
    try:
        all_time_list = []
        # Get time from PDCA
        time_before = "Noneone"
        time_after = "Nonetwo"
        # --------------------------------------------------------------------------------------------------------------
        # Table File :   Serial Number, Processor, Memorry, Storage, Keyboard, Memorry Vendor, (others tab set)
        table_time_list = []
        table_name_list = []
        table_list_result = []
        tabel_title_list = ['Serial Number', 'Processor', 'Memorry', 'Storage', 'Keyboard',
                            'Memorry Vendor', 'Bundle Name']
        table_list_result.append(serialnumber)
        # --------------------------------------------------------------------------------------------------------------
        # Test item File: Serial Number, (others test item)
        n = 0
        dict_test_item = {}
        dict_test_result = ['Serial Number']
        dictItem = plistlib.readPlist(config_test_item_path)
        item_title = []
        for i in range(len(dictItem.keys())):
            item_title.append(dictItem[str(i + 1)]['item'] + ' #' + dictItem[str(i + 1)]['code'])

        if not os.path.isfile(result_test_item_path):
            writer = csv.writer(open(result_test_item_path, 'a'))
            writer.writerow(dict_test_result + item_title)

        test_time_result = []
        test_time_result.append(serialnumber)

        # --------------------------------------------------------------------------------------------------------------
        # Test command File: Serial Number, (others test item)
        m = 0
        dict_command_item = {}
        dictCommand = plistlib.readPlist(config_command_item_path)
        command_title = ['Serial Number']
        ip = 1
        for i in range(len(dictCommand.keys()) / 2):
            dict_temp = dictCommand[str(ip)]
            if "line" in dictCommand[str(ip)]:
                command_title.append(dictCommand[str(ip)]['name'] + ' | ' + dictCommand[str(ip)]['line'])
            if "message" in dictCommand[str(ip)]:
                command_title.append(dictCommand[str(ip)]['name'] + ' | ' + dictCommand[str(ip)]['message'])
            ip = ip + 2

        if not os.path.isfile(result_command_item_path):
            writer = csv.writer(open(result_command_item_path, 'a'))
            writer.writerow(command_title)

        command_time_result = []
        command_time_result.append(serialnumber)

        # --------------------------------------------------------------------------------------------------------------

        config_path = find_file(FileName, "configExpected.txt")
        if len(config_path) > 0:
            config_path_true = config_path[0]
            storage, processor, memorry, keyboard = read_config(config_path_true)
        else:
            storage, processor, memorry, keyboard = None, None, None, None

        with open(filename) as f_obj:
            for line in f_obj:
                # ------------------------------------------------------------------------------------------------------
                if "FAIL-UPDA" in line:  # Skip Fail Log or Retry Log
                    fail_state = 1
                    break
                times = re.findall(r'[0-9]{4}/[0-9]{2}/[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}', line)
                if len(times) > 0:
                    all_time_list.append(times[0])
                if memorry_vendor == "None":  # Check Memorry Vendor
                    if "Memory" in line and "vendor:" in line:
                        vendor = re.findall('vendor:([A-Za-z]*)', line)
                        if len(vendor) > 0:
                            memorry_vendor = vendor[0]
                if Bundle == "None":  # Check Bundle Name
                    if "DTI" in line:
                        bundle_name = re.findall(r'Bundle="(.*?)"', line)
                        if len(bundle_name) > 0:
                            Bundle = str(bundle_name[0])
                # ------------------------------------------ Table -----------------------------------------------------
                if "TABL-TSTA" in line:
                    table_time = re.findall(r'[0-9]{4}/[0-9]{2}/[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}', line)
                    table_name = re.findall(r'TableName="(.*?)"', line)
                    if len(table_time) > 0:
                        table_time_list.append(table_time[0])
                    if len(table_name) > 0:
                        table_name_list.append(table_name[0])

                if "Setting time on UUT to:" in line:
                    before_time = re.findall(r'[0-9]{4}/[0-9]{2}/[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}', line)
                    after_time = re.findall(r'[0-9]{2}\-[0-9]{2}\-[0-9]{4} [0-9]{2}\:[0-9]{2}\:[0-9]{2}', line)
                    if len(before_time) > 0 and len(after_time) > 0:
                        after_time_splist = str(after_time[0]).split()[0]
                        after_time_date = str(after_time_splist).split('-')[2] + '/' + \
                                          str(after_time_splist).split('-')[0] + '/' + \
                                          str(after_time_splist).split('-')[1]
                        time_before = before_time[0]
                        time_after = str(after_time_date) + ' ' + str(after_time[0]).split()[1]
                # ---------------------------------- Test item ---------------------------------------------------------
                if "TEST-TSTT" in line:
                    code1 = re.findall(r'tid="([0-9]*)"', line)
                    name1 = re.findall(r'tname="(.*?)"', line)
                    formt1 = re.findall(r'sid="(.*?)"', line)
                    time1 = re.findall(r'[0-9]{4}/[0-9]{2}/[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}', line)

                    if len(code1) > 0 and len(name1) > 0 and len(formt1) > 0 and len(time1) > 0:
                        n = n + 1
                        test_item1 = {
                            "location": "Start",
                            "item": str(formt1[0]),
                            "code": str(code1[0]),
                            "info": str(name1[0]),
                            "time": str(time1[0])
                        }
                        dict_test_item[str(n)] = test_item1

                if "TEST-TSTP" in line:
                    code2 = re.findall(r'tid="([0-9]*)"', line)
                    formt2 = re.findall(r'sid="(.*?)"', line)
                    time2 = re.findall(r'[0-9]{4}/[0-9]{2}/[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}', line)

                    if len(code2) > 0 and len(formt2) > 0 and len(time2) > 0:
                        n = n + 1
                        test_item2 = {
                            "location": "End",
                            "item": str(formt2[0]),
                            "code": str(code2[0]),
                            "time": str(time2[0])
                        }
                        dict_test_item[str(n)] = test_item2

                # --------------------------------- Test command -------------------------------------------------------
                if "CMMD-CSTT" in line and "action.command" not in line:
                    name21 = re.findall(r'ProcessName="(.*?)"', line)
                    command_line1 = re.findall(r'CommandLine="(.*?)"', line)
                    location1 = re.findall(r'TableName="(.*?)"', line)
                    message1 = re.findall(r'Message="(.*?)"', line)
                    time3 = re.findall(r'[0-9]{4}/[0-9]{2}/[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}', line)

                    if len(name21) > 0 and len(command_line1) > 0 and len(location1) > 0 and len(time3) > 0:
                        m = m + 1
                        command_item1 = {
                            "name": str(name21[0]),
                            "line": str(command_line1[0]),
                            "location": str(location1[0]),
                            "time": str(time3[0])

                        }
                        dict_command_item[str(m)] = command_item1

                    if len(name21) > 0 and len(message1) > 0 and len(location1) > 0 and len(time3) > 0:
                        m = m + 1
                        command_item1 = {
                            "name": str(name21[0]),
                            "message": str(message1[0]),
                            "location": str(location1[0]),
                            "time": str(time3[0])
                        }
                        dict_command_item[str(m)] = command_item1
                if "CMMD-CRST" in line and "action.command" not in line:
                    name2 = re.findall(r'ProcessName="(.*?)"', line)
                    command_line2 = re.findall(r'CommandLine="(.*?)"', line)
                    location2 = re.findall(r'TableName="(.*?)"', line)
                    message2 = re.findall(r'Message="(.*?)"', line)
                    time4 = re.findall(r'[0-9]{4}/[0-9]{2}/[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}', line)

                    if len(name2) > 0 and len(command_line2) > 0 and len(location2) > 0 and len(time4) > 0:
                        m = m + 1
                        command_item2 = {
                            "name": str(name2[0]),
                            "line": str(command_line2[0]),
                            "location": str(location2[0]),
                            "time": str(time4[0])
                        }
                        dict_command_item[str(m)] = command_item2

                    if len(name2) > 0 and len(message2) > 0 and len(location2) > 0 and len(time4) > 0:
                        m = m + 1
                        command_item2 = {
                            "name": str(name2[0]),
                            "message": str(message2[0]),
                            "location": str(location2[0]),
                            "time": str(time4[0])
                        }
                        dict_command_item[str(m)] = command_item2
        del dict_command_item[str(len(dict_command_item.keys()))]

        if "ShippingSetting.ntab" not in table_name_list and "Post.ntab" in table_name_list:
            fail_state = 1

        # --------------------------------------------- Table set export -----------------------------------------------
        if fail_state == 0:
            table_list_result.append(processor)
            table_list_result.append(memorry)
            table_list_result.append(storage)
            table_list_result.append(keyboard)
            table_list_result.append(memorry_vendor)
            table_list_result.append(Bundle)

            if time_before != time_after:
                Startup1 = Time_calculate(Time_chek(table_time_list[0]), Time_chek(time_before))
                Startup2 = Time_calculate(Time_chek(time_after), Time_chek(table_time_list[1]))
                # Startup_time = time_add(Startup1, Startup2)  # -- >>
                Startup_time = int(Startup1) + int(Startup2)
                table_list_result.append(Startup_time)
                # print time_before,time_after
                j = 0
                for i in range(len(table_name_list) - 1):
                    start_time = table_time_list[j]
                    end_time = table_time_list[j + 1]
                    j = j + 1
                    left_time = Time_calculate(Time_chek(start_time), Time_chek(end_time))
                    if i != 0 or time_before == time_after:
                        table_list_result.append(left_time)

            if time_before == time_after:
                j = 0
                for i in range(len(table_name_list) - 1):
                    start_time = table_time_list[j]
                    end_time = table_time_list[j + 1]
                    j = j + 1
                    left_time = Time_calculate(Time_chek(start_time), Time_chek(end_time))
                    table_list_result.append(left_time)

            # table_list_result.append(time_add(Time_calculate(Time_chek(table_time_list[-1]), Time_chek(all_time_list[-1])), "8h0m0s"))  # -- >>
            table_list_result.append(
                str(int(Time_calculate(Time_chek(table_time_list[-1]), Time_chek(all_time_list[-1]))) + 28800))

            if not os.path.isfile(result_main_item_path):
                writer = csv.writer(open(result_main_item_path, 'a'))
                writer.writerow(tabel_title_list + table_name_list)
            writer = csv.writer(open(result_main_item_path, 'a'))
            writer.writerow(table_list_result)
            # ------------------------------------------ Test item export ----------------------------------------------

            se = 1
            for i in range(len(dictItem.keys())):
                if se < len(dict_test_item.keys()):
                    TIME_LEFT = int(Time_chek(dict_test_item[str(se + 1)]['time'])) - int(
                        Time_chek(dict_test_item[str(se)]['time']))
                    test_time_result.append(str(TIME_LEFT))
                se = se + 2
            if str(len(test_time_result)) == str(len(dictItem.keys()) + 1):
                writer = csv.writer(open(result_test_item_path, 'a'))
                writer.writerow(test_time_result)

            # ------------------------------------------ Test command export -------------------------------------------

            sr = 1
            for i in range(len(dictCommand.keys()) / 2):
                if sr < len(dict_command_item.keys()):
                    TIME_LEFT = int(Time_chek(dict_command_item[str(sr + 1)]['time'])) - int(
                        Time_chek(dict_command_item[str(sr)]['time']))
                    command_time_result.append(str(TIME_LEFT))
                sr = sr + 2
            if str(len(command_time_result)) == str(len(dictCommand.keys()) / 2 + 1):
                writer = csv.writer(open(result_command_item_path, 'a'))
                writer.writerow(command_time_result)

                # ----------------------------------------------------------------------------------------------------------

    except TypeError as e:
        print('TypeError', e)


if __name__ == '__main__':
    Path = raw_input("请输入Log路径:")

    if Path == "1":
        file = raw_input("请输入标准log(仅限processlog):")
        check_config_file(file)
        Path = raw_input("参数已经生成，请继续输入要处理的Log路径:")

    log_list = find_file(Path, ".tgz")

    print "Begin...."
    for i in log_list:
        q.put(i)
    print "Job Qsize:", q.qsize()
    for x in range(NUM_WORKERS):
        MyThread(q, x).start()
