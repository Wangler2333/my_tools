#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time     : 2018/1/13下午3:32
# @Author   : Saseny Zhou
# @Site     : 
# @File     : PCle_Collection_Log.py
# @Software : PyCharm Community Edition


import time
import os
import commands
import shutil


class PCLe(object):
    def __init__(self, targetPath):
        self.logPath = "/var/tmp"
        self.targetPath = targetPath
        self.currentTime = str(int(time.time()))
        self.folderPath = os.path.join(self.targetPath, self.currentTime)
        self.createFolder(self.folderPath)

    def findCsv(self):
        for i in os.listdir(self.logPath):
            if str(i).endswith(".csv"):
                yield os.path.join(self.logPath, str(i))

    def createFolder(self, path):
        if not os.path.isdir(path):
            os.makedirs(path)

    def writeFile(self, string, path):
        try:
            f = open(path, 'a')
            f.write(str(string))
            f.close()
        except:
            print("Write File Fail.")

    def runShell(self):
        hardInfo = commands.getoutput("system_profiler SPHardwareDataType")
        self.writeFile(hardInfo, os.path.join(self.folderPath, "HardInfo.txt"))

    def copyFile(self):
        for i in self.findCsv():
            shutil.copy(i, self.folderPath)

    def run(self):
        self.runShell()
        self.copyFile()


if __name__ == '__main__':
    t = PCLe("/Phoenix/Logs/")
    t.run()
