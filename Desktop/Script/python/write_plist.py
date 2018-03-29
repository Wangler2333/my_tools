#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import plistlib
import sys
import os

file_path = '/Users/saseny/Desktop/GeneralPreference.plist'


def writeFIle(*args):
    dict = plistlib.readPlist(file_path)
    dict['Site_Preference']['Comms']['Discover'] = args[0]
    dict['Site_Preference']['Comms']['Default_CTS_IP'] = args[1]
    plistlib.writePlist(dict, file_path)


def main(parameter):
    if parameter == '0':
        writeFIle('0', '127.0.0.1')
    elif parameter == '1':
        writeFIle('1', '10.0.0.85')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        os._exit(1)
    parameter = sys.argv[1]
    main(parameter)
