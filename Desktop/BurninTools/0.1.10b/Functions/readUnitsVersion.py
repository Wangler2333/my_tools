#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time     : 2018/3/17上午9:44
# @Author   : Saseny Zhou
# @Site     : 
# @File     : readUnitsVersion.py
# @Software : PyCharm


from Config.versionRead import *
from Functions.observation import *


class DTIDetailVersion():
    def __init__(self, configInfo):
        self.configInfo = configInfo
        self.cmdPath = "/tmp/getVersion.sh"
        self.targetPath = os.path.join(os.path.expanduser("~"), "Desktop")

    def write_command(self):
        f = open(self.cmdPath, 'a')
        f.write(SystemVersionReadCommand)
        f.close()
        shell("chmod 777 %s" % self.cmdPath)

    def running(self):
        self.write_command()
        t = Observation(self.configInfo)
        dtiInfo = t.getDti()
        code, _ = shell(" ".join([self.cmdPath, os.path.join(self.targetPath, dtiInfo + ".txt")]))
        os.system("rm -rf %s" % self.cmdPath)
        if code == 0:
            return True
        else:
            return False
