#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Create by Saseny on 2017/06/28


import threading
import Queue
import os
import re
import glob
import time
import csv
import sys

q = Queue.Queue(0)
NUM_WORKERS = 10
mylock = threading.Lock()

print "\033[1;32m" + '''
输出文件在脚本同目录下 result_for_check 文件夹下:

 -  1 Table_left_time.csv 所有测试tab时间;
 -  2 Item_left_time.csv 所有测试项目时间，由于用的是列表存储数值，所以会存在bug;
 -  3 Command_left_time.csv 所有测试command时间，bug同上.

-->> 设 置： 跳过CQA Log, 以及跳过有(Fail)或者(Retry)的Log,
     注 意： 拖入log路径之后请删除路径最后的空格, Log 压缩文件必须以(.tgz)结尾.

''' + "\033[0m"


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


def Time_chek(_time):
    try:
        timeArray = time.strptime(_time, "%Y/%m/%d %H:%M:%S")
        timeStamp = int(time.mktime(timeArray))
        return timeStamp
    except UnboundLocalError as p:
        print ('UnboundLocalError', p)


def Time_calculate(Start, End):
    d = int(End) - int(Start)
    hour = d / 3600
    d1 = d % 3600
    min = d1 / 60
    d2 = d1 % 60
    time = str(hour) + "h" + str(min) + "m" + str(d2) + "s"
    return time


def check_Memory_vonder(filepath):
    try:
        c = []
        with open(filepath) as gs:
            for line in gs:
                if "Memory" in line and "vendor:" in line:
                    c.append(line.split('"')[11].split(':')[-1])
            if c:
                return str(c[0])
            else:
                return None
    except IOError as oi:
        print ('IOError', oi)


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


def read_config(path):
    SSD = None ; CPU = None ; Memory = None
    with open(path) as f:
        for line in f:
            ssd = re.findall(r'devicecapacity = "(.*?)"', line)
            cpu = re.findall(r'frequency = "(.*?)"', line)
            memory = re.findall(r'size = "(.*?)"', line)
            keyboard = re.findall(r'identifier = "Apple Internal Keyboard / Trackpad" & language = "(.*?)"', line)

            if len(ssd) > 0:
                SSD = ssd[0]
            if len(cpu) > 0:
                CPU = float(float(cpu[0]) / 1000)
            if len(memory) > 0:
                Memory = memory[0]
        result = str(CPU) + 'GHz/' + str(Memory) + 'GB/' + str(SSD) + 'GB'
    return result


def doJob(job, worktype):
    global Number
    file = str(job)
    filepath = os.path.dirname(file)
    os.system('cd %s ; tar -zxf %s &>/dev/null' % (filepath, file))
    FileName = file.replace('.tgz', '')
    de = re.findall(r'C02[A-Z]\w{8}', FileName)
    if de:
        SerialNumber = de[0]
    r = glob.glob(FileName + '/*/processlog.plog')
    t = glob.glob(FileName + '/*/*/processlog.plog')
    Running = False
    # Check config
    config_path = find_file(FileName, "configExpected.txt")
    if len(config_path) > 0:
        config_path_true = config_path[0]
        configinfo = read_config(config_path_true)
    else:
        configinfo = None
    if r:
        LogPoath = r[0]
        Running = True
    if t:
        LogPoath = t[0]
        Running = True

    if Running == True:
        # check Memory vendor
        Vendor_memorry = check_Memory_vonder(LogPoath)
        info = str(configinfo) + ' ' + str(Vendor_memorry)
        # print "doing", LogPoath, " --- Thread@ " + str(worktype) + " Start"
        print "Doing -- [" + str(SerialNumber) + "] --- Thread@ " + str(worktype) + " Start"
        mylock.acquire()
        Processing(LogPoath, SerialNumber, info)
        # print "doing", LogPoath, " --- Thread@ " + str(worktype) + " End"
        print "Done  -- [" + str(SerialNumber) + "] --- Thread@ " + str(worktype) + " End"
        os.system('rm -rf %s' % FileName)
        mylock.release()
    else:
        print "\033[0;31m" + "doing", FileName, " --- worktype Log Was Wrong -Thread@ ", str(worktype) + "\033[0m"
        # print "\033[0;31m" + "Doing -- [" + str(SerialNumber) + "] --- worktype Log Was Wrong -Thread@ ", str(worktype) + "\033[0m"
        os.system('rm -rf %s' % FileName)


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


def Bundle_Check(file):
    try:
        b = []
        with open(file) as sg:
            for line in sg:
                if "DTI" in line:
                    ad = re.findall(r'Bundle="(.*?)"', line)
                    if len(ad) > 0:
                        b.append(ad[0])
            return b[1]
    except IOError as f:
        print ('IOError_3:', f)


def Processing(filename, sn, configinfo):
    try:
        bundle_name = Bundle_Check(filename)
        # Table 集合声明
        time_list = []
        table_name_list = []
        msg_type_list = []
        all_times = []
        result_item = []
        result_value = []
        result_item.append("Serial Number")
        result_item.append("Config Info and Memory Vendor")
        result_item.append("Bundle Name")
        result_value.append(sn)
        result_value.append(configinfo)
        result_value.append(bundle_name)

        # Item 集合声明 和 参数设置
        item_start = "TEST-TSTT"
        item_end = "TEST-TSTP"
        item_time_strat_list = []
        item_time_end_list = []
        item_list = []
        item_left_time = []
        item_list_title = []
        item_list_value = []
        item_list_title.append('Serial Number')
        item_list_value.append(sn)

        # Command 集合声明 和 参数设置
        command_start = "CMMD-CSTT"
        command_end = "CMMD-CRST"
        command_time_start_list = []
        command_time_end_list = []
        command_list = []
        command_list_title = []
        command_list_value = []
        command_list_title.append('Serial Number')
        command_list_value.append(sn)

        write = True
        time_start_do = False
        aeo = 0
        aey = 0

        if "CQA" not in filename:
            with open(filename) as f:

                for line in f:
                    # table 时间和名字收集
                    times = re.findall(r'[0-9]{4}/[0-9]{2}/[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}', line)
                    if len(times) > 0:
                        all_times.append(times[0])
                    msg = re.findall(r'msg-type="(.*?)"', line)
                    if len(msg) > 0:
                        msg_type_list.append(msg[0])
                    if "TABL-TSTA" in line:
                        time = re.findall(r'[0-9]{4}/[0-9]{2}/[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}', line)
                        table_name = re.findall(r'TableName="(.*?)"', line)
                        if len(time) > 0:
                            time_list.append(time[0])
                        if len(table_name) > 0:
                            table_name_list.append(table_name[0])

                    # item 时间和名字收集
                    if item_start in line:
                        t = re.findall(r'[0-9]{4}/[0-9]{2}/[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}', line)
                        if len(t) > 0:
                            item_time_strat_list.append(t[0])
                        n = re.findall(r'tid="([0-9]*)"', line)
                        s = re.findall(r'sid="(.*?)"', line)
                        if len(n) > 0 and len(s) > 0:
                            ns = str(s[0]) + ' #' + str(n[0])
                            item_list.append(ns)
                    if item_end in line:
                        e = re.findall(r'[0-9]{4}/[0-9]{2}/[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}', line)
                        if len(e) > 0:
                            item_time_end_list.append(e[0])

                    if "FAIL-UPDA" in line:
                        write = False

                    # command 时间和名字收集
                    if command_start in line:
                        r = re.findall(r'[0-9]{4}/[0-9]{2}/[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}', line)
                        if len(r) > 0:
                            command_time_start_list.append(r[0])
                        o = re.findall(r'ProcessName="(.*?)"', line)
                        l = re.findall(r'CommandLine="(.*?)"', line)
                        if len(o) > 0 and len(l) > 0:
                            ol = str(o[0]) + ' -' + str(l[0])
                            command_list.append(ol)
                        elif len(o) > 0 and len(l) == 0:
                            command_list.append(o[0])
                    if command_end in line:
                        w = re.findall(r'[0-9]{4}/[0-9]{2}/[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}', line)
                        if len(w) > 0:
                            command_time_end_list.append(w[0])

                    # Comm.Get.Time 时间
                    if "Setting time on UUT" in line:
                        a1 = re.findall(r'[0-9]{4}/[0-9]{2}/[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}', line)
                        a2 = re.findall(r'[0-9]{2}-[0-9]{2}-[0-9]{4} [0-9]{2}:[0-9]{2}:[0-9]{2}', line)

                        if len(a1) > 0 and len(a2) > 0:
                            date = str(a2[0]).split()[0]
                            r_date = str(date).split('-')[2] + '/' + str(date).split('-')[0] + '/' + \
                                     str(date).split('-')[1] + ' ' + str(a2[0]).split()[1]
                            date1 = str(a1[0]).split()[0]
                            date2 = str(date).split('-')[2] + '/' + str(date).split('-')[0] + '/' + \
                                    str(date).split('-')[1]
                            if str(date).split('-')[2] + '/' + str(date).split('-')[0] + '/' + \
                                    str(date).split('-')[1] != date1:
                                time_set_before = a1[0]
                                time_set = r_date
                                time_start_do = True
                    # Get run-in time

                    if "Runin_Battery.ntab" in line and "TABL-TSTA" in line:
                        run_in_start_ = re.findall(r'[0-9]{4}/[0-9]{2}/[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}', line)
                        if len(run_in_start_) > 0:
                            run_in_start = run_in_start_[0]
                            aeo = 1

                    if "Runin_Fail.ntab" in line and "TABL-TSTA" in line:
                        run_in_end_ = re.findall(r'[0-9]{4}/[0-9]{2}/[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}', line)
                        if len(run_in_end_) > 0:
                            run_in_end = run_in_end_[0]
                            aey = 1

            if aeo == 1 and aey == 1:
                run_in_time = Time_calculate(Time_chek(run_in_start),Time_chek(run_in_end))
            else:
                run_in_time = None

            if write == True:
                # Startup.ntab time
                if time_start_do == True:
                    Startup1 = Time_calculate(Time_chek(time_list[0]), Time_chek(time_set_before))
                    Startup2 = Time_calculate(Time_chek(time_set), Time_chek(time_list[1]))
                    Startup_time = time_add(Startup1, Startup2)
                    result_value.append(Startup_time)
                # table 时间以及打印
                j = 0
                for i in range(len(table_name_list) - 1):
                    start_time = time_list[j]
                    end_time = time_list[j + 1]
                    j = j + 1
                    left_time = Time_calculate(Time_chek(start_time), Time_chek(end_time))
                    if i != 0 or time_start_do == False:
                        result_value.append(left_time)
                result_value.append(
                    time_add(Time_calculate(Time_chek(time_list[-1]), Time_chek(all_times[-1])), "8h0m0s"))
                result_value.append(run_in_time)

                if not os.path.isfile(Resultpath):
                    red = result_item + table_name_list
                    red.append("Run-in Time Left")
                    writer = csv.writer(open(Resultpath, 'a'))
                    writer.writerow(red)

                writer = csv.writer(open(Resultpath, 'a'))
                writer.writerow(result_value)

                # item 时间以及打印
                for i in range(len(item_time_end_list)):
                    left_time_item = int(Time_chek(item_time_end_list[i])) - int(Time_chek(item_time_strat_list[i]))
                    item_left_time.append(left_time_item)

                if not os.path.isfile(Resultpath_item):
                    reds = item_list_title + item_list
                    writer = csv.writer(open(Resultpath_item, 'a'))
                    writer.writerow(reds)
                reod = item_list_value + item_left_time
                writer = csv.writer(open(Resultpath_item, 'a'))
                writer.writerow(reod)

                # command 时间以及打印
                # print len(command_list), len(command_time_start_list), len(command_time_end_list)
                for i in range(len(command_time_end_list)):
                    left_time_item = int(Time_chek(command_time_end_list[i])) - int(
                        Time_chek(command_time_start_list[i]))
                    command_list_value.append(left_time_item)

                if not os.path.isfile(Resultpath_command):
                    reds = command_list_title + command_list
                    writer = csv.writer(open(Resultpath_command, 'a'))
                    writer.writerow(reds)
                reod = command_list_value
                writer = csv.writer(open(Resultpath_command, 'a'))
                writer.writerow(reod)

                a = set(msg_type_list)
                b = []
                for i in a:
                    b.append(i)
            else:
                print '-->> ' + str(sn) + " - Had retry or fail in it so we needn't this log for use."
        else:
            print '-->> ' + str(sn) + ' was CQA test log.'

    except TypeError as e:
        print('UnboundLocalError', e)


if __name__ == '__main__':
    Path = raw_input("请输入Log路径:")
    Date = time.strftime("%Y_%m_%d_%H_%M_%S")
    root_path = os.path.dirname(sys.argv[0]) + '/result_for_check'
    os.system('mkdir -p %s' % root_path)
    Resultpath = root_path + '/Table_left_time.csv'
    Resultpath_item = root_path + '/Item_left_time.csv'
    Resultpath_command = root_path + '/Command_left_time.csv'

    a = find_file(Path, ".tgz")
    print "Begin...."
    for i in a:
        q.put(i)
    print "Job Qsize:", q.qsize()
    for x in range(NUM_WORKERS):
        MyThread(q, x).start()
