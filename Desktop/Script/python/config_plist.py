#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Create by Saseny on 2017/07/01

import os
import re
import sys
import plistlib


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
    for i in range(210):
        if str(command[str(j)]) == str(command[str(j + 1)]):
            a = 1
        if str(command[str(j)]) != str(command[str(j + 1)]):
            b = 1
        j = j + 2

    if a == 1 and b != 1:
        plistlib.writePlist(command, filename)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        exit(1)
    file = sys.argv[1]

    os.system('mkdir -p %s' % os.path.dirname((sys.argv[0])) + '/CONFIG/')

    result_for_item = os.path.dirname((sys.argv[0])) + '/CONFIG/' + 'item_Expected.plist'
    result_for_command = os.path.dirname((sys.argv[0])) + '/CONFIG/' + 'command_Expected.plist'

    os.system('rm -rf %s' % os.path.dirname((sys.argv[0])) + '/CONFIG/*')

    item_check(file, result_for_item)
    command_check(file, result_for_command)
