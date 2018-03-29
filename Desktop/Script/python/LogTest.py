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
import plistlib
import json


def Time_chek(_time):
    try:
        timeArray = time.strptime(_time, "%Y/%m/%d %H:%M:%S")
        timeStamp = int(time.mktime(timeArray))
        return timeStamp
    except UnboundLocalError as p:
        print ('UnboundLocalError', p)


def item_check():
    item = {}
    n = 0
    file = "/Users/sasenyzhou/Desktop/DOE/processlog.plog"
    running = True
    with open(file) as f:
        for line in f:

            if "TEST-TSTT" in line:
                n = n + 1

                code = re.findall(r'tid="([0-9]*)"', line)
                name = re.findall(r'tname="(.*?)"', line)
                time = re.findall(r'ts="(.*?)"', line)
                formt = re.findall(r'sid="(.*?)"', line)

                # print len(code), len(name), len(time)

                if len(code) > 0 and len(name) > 0 and len(time) > 0 and len(formt) > 0:
                    named = str(formt[0]) + ' #' + str(code[0]) + ' ' + str(name[0])
                    test_item = {"code":str(code[0]),
                                 "time":str(time[0]),
                                 "name":str(named)}

                    # print test_item

                    item[str(n)] = test_item

            if "TEST-TSTP" in line:
                n = n + 1
                code = re.findall(r'tid="([0-9]*)"', line)
                time = re.findall(r'ts="(.*?)"', line)

                # print len(code), len(name), len(time)

                if len(code) > 0 and len(time) > 0:
                    test_item = {"code":str(code[0]),
                                 "time":str(time[0])}

                    # print test_item

                    item[str(n)] = test_item

        plistlib.writePlist(item, "/Users/sasenyzhou/Desktop/DOE/item_test.plist")
        filename = "/Users/sasenyzhou/Desktop/DOE/configExpected.json"
        with open(filename,'w') as f_obj:
            json.dump(item,f_obj)
        print n

        if n % 2 != 0:
            print "Item Log was abnormal : " + str(n)
            running = False
    if running == True:

        r_m = plistlib.readPlist("/Users/sasenyzhou/Desktop/DOE/item_test.plist")

        j = 1
        for i in range(n / 2):
            dict1 = r_m[str(j)]
            dict2 = r_m[str(j + 1)]
            j = j + 2

            #print dict1
            #print dict2


            #print dict1.values()[0][1]
            # print dict1.values()[0][0], dict2.values()[0]
            #print int(Time_chek(dict2.values()[0])) - int(Time_chek(dict1.values()[0][0]))


def command_check():
    command = {}
    n = 0
    file = "/Users/sasenyzhou/Desktop/DOE/processlog.plog"
    running = True
    with open(file) as f:
        for line in f:

            if "CMMD-CSTT" in line:
                n = n + 1

                name = re.findall(r'ProcessName="(.*?)"', line)
                line_ = re.findall(r'CommandLine="(.*?)"', line)
                time = re.findall(r'ts="(.*?)"', line)

                if len(name) > 0 and len(line_) > 0 and len(time) > 0:
                    command_item = str(name[0]) + ':' + str(line_[0])
                    if "action.command" not in line_[0]:
                        command[str(n)] = [str(command_item), str(time[0])]
                    else:
                        n = n - 1
                elif len(name) > 0 and len(line_) == 0 and len(time) > 0:
                    command[str(n)] = [str(name[0]), str(time[0])]

            if "CMMD-CRST" in line:
                n = n + 1

                name = re.findall(r'ProcessName="(.*?)"', line)
                line_ = re.findall(r'CommandLine="(.*?)"', line)
                time = re.findall(r'ts="(.*?)"', line)

                if len(name) > 0 and len(line_) > 0 and len(time) > 0:
                    command_item = str(name[0]) + ':' + str(line_[0])
                    if "action.command" not in line_[0]:
                        command[str(n)] = [str(command_item), str(time[0])]
                    else:
                        n = n - 1
                elif len(name) > 0 and len(line_) == 0 and len(time) > 0:
                    command[str(n)] = [str(name[0]), str(time[0])]

        plistlib.writePlist(command, "/Users/sasenyzhou/Desktop/DOE/command_test.plist")
        print n

        if n % 2 == 0:
            print "Command Log was abnormal : " + str(n)
            running = False
    if running == True:

        r_m = plistlib.readPlist("/Users/sasenyzhou/Desktop/DOE/command_test.plist")

        j = 1
        for i in range(n / 2):
            dic1 = r_m[str(j)]
            dic2 = r_m[str(j + 1)]
            j = j + 2

            #print dic1
            #print dic2


            #print dic1[0]
            # print dic1[1], dic2[1]
            #print int(Time_chek(dic2[1])) - int(Time_chek(dic1[1]))


item_check()
command_check()
