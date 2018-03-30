#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time     : 2018/3/17下午3:19
# @Author   : Saseny Zhou
# @Site     : 
# @File     : versionRead.py
# @Software : PyCharm


SystemVersionReadRule = {
    "system":
        {
            1:
                {
                    "name": "OS Version",
                    "cmd": "system_profiler SPSoftwareDataType",
                    "key": "System Version:"
                },
            2:
                {
                    "name": "BootRom Version",
                    "cmd": "system_profiler SPHardwareDataType",
                    "key": "Boot ROM Version:"
                },
            3:
                {
                    "name": "SMC Version",
                    "cmd": "system_profiler SPHardwareDataType",
                    "key": "SMC Version:"
                },
            4:
                {
                    "name": "Model",
                    "cmd": "system_profiler SPHardwareDataType",
                    "key": "Model Identifier:"
                },
            5:
                {
                    "name": "BlueTooth Version",
                    "cmd": "system_profiler SPBluetoothDataType",
                    "key": "Firmware Version:"
                },
            6:
                {
                    "name": "ThunderBolt Version",
                    "cmd": "system_profiler SPThunderboltDataType",
                    "key": "Firmware Version:"
                },
            7:
                {
                    "name": "TrackPad ST Version",
                    "cmd": "system_profiler SPSPIDataType",
                    "key": "Version:"
                },
            8:
                {
                    "name": "Mac ID",
                    "cmd": "ioreg -l",
                    "key": "board-id"
                },
            9:
                {
                    "name": "AirPort Version",
                    "cmd": "system_profiler SPAirPortDataType",
                    "key": "Firmware Version:"
                }
        },
    "plugin": "/AppleInternal/Diagnostics/OS/Plugins",
    "Frameworks": "/Library/Frameworks",
    "command": "kextstat"
}
