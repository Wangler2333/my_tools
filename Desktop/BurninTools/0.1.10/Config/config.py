#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time     : 2018/3/15上午10:17
# @Author   : Saseny Zhou
# @Site     : 
# @File     : config.py
# @Software : PyCharm


configInfo = {
    "function":
        {
            "Observation":
                {
                    "collection log": False,
                    "default": False
                },
            "Yield Report":
                {
                    "collection log": True,
                    "default": False
                },
            "Log Collection":
                {
                    "collection log": False,
                    "default": False
                },
            "Observation Report":
                {
                    "collection log": False,
                    "default": False
                },
            "Detail DTI Info":
                {
                    "collection log": False,
                    "default": False
                }
        },
    "process":
        {
            "Log Path":
                {
                    "default": True,
                    "set path": ""
                },
            "DTI Read":
                {
                    "file path": "/",
                    "file name": "release_notes.html",
                    "read rule": "(J132_EVT_\\d+.+)"
                },
            "Serial Number":
                {
                    "command": "system_profiler SPHardwareDataType",
                    "read rule": "C02[A-Z].{8}"
                },
            "gOS Files":
                {
                    "failures.csv": True,
                    "summary.csv": True
                },
            "MacOS Files":
                [

                ],
            "Special Request":
                [
                    "2696",
                    "2697"
                ],
            "Excel Read":
                {
                    "file name": "Error_Code.xlsx",
                    "sheet name": "Error Codes",
                    "location":
                        {
                            "code": 2,
                            "error": 4
                        },
                    "station":
                        [
                            "Run-in",
                            "Log collection"
                        ]
                },
            "failure read":
                {
                    "replace": "/1",
                    "combination":
                        {
                            "name": 1,
                            "states": 10
                        },
                    "Fail Keys":
                        [
                            "FAIL",
                            "TIMEOUT"
                        ],
                },
            "Unit Number":
                {
                    "file name": "Units_Info.xlsx",
                    "sheet name": "units",
                    "location":
                        {
                            "serial number": 0,
                            "unit number": 1,
                            "config info": 2
                        }
                },
            "exception":
                {
                    "default": False,
                    "list":
                        [

                        ]
                }
        }
}
