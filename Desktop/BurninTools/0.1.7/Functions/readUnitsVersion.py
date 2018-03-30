#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time     : 2018/3/17上午9:44
# @Author   : Saseny Zhou
# @Site     : 
# @File     : readUnitsVersion.py
# @Software : PyCharm

from Path.path import *
from Functions.shell import *
from Config.versionRead import *


class DTIDetailVersion():
    def __init__(self, configInfo):
        self.configInfo = configInfo

    def run(self):
        for i in range(len(self.configInfo["system"])):
            info = self.configInfo["system"][i + 1]
            code, record = shell(info["cmd"])
            self.check(record, info)

    def check(self, record, info):
        for i in record:
            if info["key"] in i:
                print(info["name"], i)


t = DTIDetailVersion(SystemVersionReadRule)
t.run()
