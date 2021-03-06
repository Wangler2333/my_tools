#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time     : 2017/12/9上午8:41
# @Author   : Saseny Zhou
# @Site     : 
# @File     : config_info.py
# @Software : PyCharm Community Edition


congfig_info = {
    "download": {
        "cmd link": "running.sh",
        "file key": "Restore",
        "suffix": ".xls"
    },
    "product_info": {
        "J79A": {
            "line": [
                "F6-1FT-C16",
                "F6-1FT-D16",
                "F6-2FT-F16",
                "F6-2FT-G16"
            ],
            "station": [
                "PRE-SWDL",
                "PRE-PI-ROUTER",
                "FACT",
                "BUTTON-TEST",
                "WIFI-THROUGHPUT",
                "WIFI-BT-OTA",
                "COEX1",
                "NAND-STATS",
                "SW-DOWNLOAD",
                "RGBW",
                "FLICKER",
                "LCD-UNIFORMITY",
                "FOS",
                "GRAPE-TEST",
                "POST-PI-ROUTER",
                "IMPEDANCE TEST"
            ]
        },
        "J80A": {
            "line": [
                "F6-2FT-H16",
                "F6-2FT-J16",
                "F6-2FT-I16"
            ],
            "station": [
                "PRE-SWDL",
                "PRE-PI-ROUTER",
                "FACT",
                "BUTTON-TEST",
                "WIFI-THROUGHPUT",
                "WIFI-BT-OTA",
                "COEX1",
                "SW-DOWNLOAD",
                "RGBW",
                "FLICKER",
                "LCD-UNIFORMITY",
                "FOS",
                "GRAPE-TEST",
                "POST-PI-ROUTER",
                "IMPEDANCE TEST"
            ]
        }
    },
    "cycle_setup": {
        "run": True,
        "time": 86400,
        "times": 10000
    },
    "user_info": {
        "user name": "",
        "pass word": ""
    },
    "external command": {
        "run": False,
        "command name": "",
        "command path": "",
        "command usage": ""
    },
    "auto_path": "",
    "retry times": 3
}
