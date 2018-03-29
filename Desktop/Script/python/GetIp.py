#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import commands
import re
import os
import sys
import time

times_out = 60
current_times = 0


def writefile(string, file):
    try:
        with open(file, 'a') as d:
            d.write(string + '\n')
    except IOError as i:
        print ('IOError:', i)


while [True]:

    if current_times == 0:
        Date = time.strftime("%Y_%m_%d_%H_%M_%S")
        file_out = os.path.dirname(sys.argv[0]) + '/' + Date + '.txt'

    IP = re.findall(r'192.\d*.\d*.\d*', commands.getoutput('ifconfig'))

    for ip in IP:
        current_times += 1
        Time = commands.getoutput('date +%Y-%m-%d_%H:%M:%S')
        State = commands.getoutput('ping -c 1 -t 1 %s | grep "loss"' % ip)
        if "100.0% packet loss" in State:
            state_ping = "FAIL"
        if "0.0% packet loss" in State:
            state_ping = "PASS"

        print str(Time) + '\t' + str(state_ping)
        Result = '[' + str(Time) + ']\t[' + str(ip) + ']\t[' + str(State) + ']\t[' + str(state_ping) + ']'
        writefile(Result,file_out)
        time.sleep(1)

    if current_times == times_out:
        current_times = 0
        a = 0
        with open(file_out) as f_job:
            for line in f_job:
                if "FAIL" in line:
                    a = 1
            if a == 1:
                change_name = str(file_out).replace('.txt','') + '_FAIL.txt'
                os.system('mv %s %s'%(file_out,change_name))
            if a == 0:
                change_name = str(file_out).replace('.txt', '') + '_PASS.txt'
                os.system('mv %s %s' % (file_out, change_name))