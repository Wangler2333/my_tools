#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time     : 2018/3/15下午2:50
# @Author   : Saseny Zhou
# @Site     : 
# @File     : threadForUI.py
# @Software : PyCharm


from PyQt5.QtCore import *
from Functions.yield_report import *
from Logs.unitLog import *


def copy_log(target_folder):
    dict_ = {'debug': False, 'finder': False, }
    dict_['destination'] = target_folder
    dict_['name'] = time.strftime("Logs-%Y-%m-%d-%H-%M-%S")
    dict_['sshpath'] = None
    dict_['targz'] = None
    return dict_


class TimeCalculate(QThread):
    timeSignal = pyqtSignal(str)

    def __init__(self, parent=None):
        super(TimeCalculate, self).__init__(parent)
        self.running = True
        self.count = 0

    def stop(self):
        self.running = False

    def run(self):
        while self.running:
            time.sleep(0.1)
            self.count += 0.1
            self.timeSignal.emit(str(round(self.count, 2)))


class WorkRunning(QThread):
    runSignal = pyqtSignal(dict)

    def __init__(self, configInfo, action, unitsInfo, errorInfo, parent=None):
        super(WorkRunning, self).__init__(parent)
        self.configInfo = configInfo
        self.action = action
        self.unitsInfo = unitsInfo
        self.errorInfo = errorInfo

    def run(self):
        if self.action == "Observation":
            t = Observation(self.configInfo)
            info = t.special()
            tmpDict = {
                "action": self.action,
                "result": {
                    "serial number": info[0],
                    "dti info": info[1],
                    "special": info[2],
                    "path road": info[3]
                },
                "finished": True
            }
            self.runSignal.emit(tmpDict)

        if self.action == "Yield Report":
            t = YieldReport(self.configInfo)
            info = t.compare(self.unitsInfo, self.errorInfo)
            tmpDict = {
                "action": self.action,
                "result": {
                    "serial number": info["serial number"],
                    "dti info": info["dti info"],
                    "path road": info["folder"]
                },
                "show error": True,
                "finished": False,
                "message": "不良代码比对完成!",
                "info": info
            }
            self.runSignal.emit(tmpDict)
            time.sleep(0.5)
            tmpDict["show error"] = False

            if self.configInfo["function"][self.action]["collection log"] is True:
                tmpDict["message"] = "开始收Log,请等待..."
                time.sleep(0.5)
                self.runSignal.emit(tmpDict)
                log_running_do(copy_log(info["folder"]))
                tmpDict["message"] = "Log收集完成!"
                time.sleep(0.5)
                self.runSignal.emit(tmpDict)

            tmpDict["finished"] = True
            time.sleep(0.5)
            self.runSignal.emit(tmpDict)

        if self.action == "Log Collection":
            t = YieldReport(self.configInfo)
            folder, _, _ = t.ready(self.unitsInfo)
            tmpDict = {
                "action": self.action,
                "message": "开始收Log,请等待...",
                "finished": False
            }
            time.sleep(0.5)
            self.runSignal.emit(tmpDict)
            log_running_do(copy_log(folder))
            tmpDict["message"] = "Log收集完成!"
            tmpDict["finished"] = True
            time.sleep(0.5)
            self.runSignal.emit(tmpDict)
