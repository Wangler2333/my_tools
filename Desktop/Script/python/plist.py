#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time     : 2017/11/29上午8:56
# @Author   : Saseny Zhou
# @Site     : 
# @File     : plist.py
# @Software : PyCharm Community Edition

import plistlib
import os

scp_cmd = '/usr/local/bin/eos-scp eos:/private/var/logs/Earthbound/%s %s'
version = '1.2'

config = {
    'check_sum': '708b668b8b3fa0da6e78aa7bb141073ea569fcc161bcc198f433cdd330b7c0c0',
    'dti_read':
        {
            'file_path': '/DTI\ Info/',
            'file_name': 'release_notes.html',
            'read_rule': 'DTI: (.*?)<br/>'
        },
    'copy_files':
        {
            'gOS_files':
                {
                    'failures.csv': True,
                    'summary.csv': False,
                },
            'Mac_files':
                {
                    '/AppleInternal/Diagnostics/Logs/testd.log': False
                },
        },
    'define_path':
        {
            'bool': False,
            'path': '/Users/saseny/Desktop/J132/_tools/'
        },
    'csv_read':
        {
            'read_key': ['PDCA Key', 'Status Code'],
        },
    'sn_read':
        {
            'cmd': 'system_profiler SPHardwareDataType',
            'read_rule': 'C02[A-Z].{8}',
        },
    'xlsx_read':
        {
            'station': ['Run-in', 'Log collection'],
            'sheet_name': 'Error Codes',
            'station_column': 3,
            'column': [4, 2, 3]
        },
    'test_logs':
        {
            'format': '.tgz',
            'cmd': 'cd %s; tar -zxf %s',
            'failures': 'bridgeOS/private/var/logs/Earthbound/Earthbound/failures.csv'
        },
    'collection_log':
        {
            'debug': False,
            'finder': False,
        },
    'open_result': True,
    'report_dti_rule': 'J132',
    'thread_max': 5,
    'system info':
        {
            'cmd':
                {
                    'system_profiler SPHardwareDataType':
                        {
                            'read_list':
                                {
                                    'Model Identifier': False,
                                    'Processor Name': False,
                                    'Processor Speed': True,
                                    'Number of Processors': False,
                                    'Total Number of Cores': False,
                                    'L2 Cache (per Core)': False,
                                    'L3 Cache': False,
                                    'Memory': True,
                                    'Bus Speed': False,
                                    'Boot ROM Version': False,
                                    'Serial Number': True,
                                    'Hardware UUID': False,
                                }
                        },
                },
            'SSD':
                {
                    'cmd': 'diskutil list | grep "GUID_partition_scheme\" | grep \"disk0\" | awk \'{print$3}\'',
                    'read': True
                },
            'Firmware':
                {
                    'TBT': 'system_profiler SPThunderboltDataType | grep \"Firmware Version\" | head -1 | sed \'s/.*: //\'',
                    # 'Bluetooth': 'system_profiler SPBluetoothDataType | grep \"Firmware Version\" | sed \'s/.*: //\'',
                    'Battery': 'system_profiler SPPowerDataType | grep \"Firmware Version\" | head -1 | sed \'s/.*: //\'',
                },
        },
    'Exception List':
        {
            'nand_performance/Storage 8041 Write Performance Test (Exit code: 1)': {'SSD': ['1T', '2T']},
            'EyeSurf/PHY_3_LANE_3_MODE_AXIS/EYE_HEIGHT (Exit code: 1)': True,
            'EyeSurf/PHY_3_LANE_3_MODE_AXIS/EYE_WIDTH (Exit code: 1)': True,
            'EyeSurf/PHY_3_LANE_0_MODE_AXIS/EYE_HEIGHT (Exit code: 1)': True
        },
    'version': version

}


def write_plist(path, obj=config, force=False):
    if not os.path.isfile(path) or force is True:
        plistlib.writePlist(obj, path)


def read_plist(path):
    if os.path.isfile(path):
        return plistlib.readPlist(path)
    else:
        return False
