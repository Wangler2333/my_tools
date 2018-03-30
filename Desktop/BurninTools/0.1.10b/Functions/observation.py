#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time     : 2018/3/15下午3:09
# @Author   : Saseny Zhou
# @Site     : 
# @File     : observation.py
# @Software : PyCharm

from collections import OrderedDict
from Functions.shell import *
from Functions.excel_read import *


class Observation():
    def __init__(self, configInfo):
        self.copy_cmd = "/usr/local/bin/eos-scp eos:%s %s"
        self.configInfo = configInfo["process"]
        if self.configInfo["Log Path"]["default"] is True:
            self.target_folder = resources
        else:
            self.target_folder = self.configInfo["Log Path"]["set path"]

    def getSn(self):
        sn = "None"
        code, getInfo = shell(self.configInfo["Serial Number"]["command"])
        if code == 0:
            for i in getInfo:
                tmp = match(self.configInfo["Serial Number"]["read rule"], i)
                if len(tmp) > 0:
                    sn = tmp[0]
                    break
        return sn

    def create(self, sn):
        current_path = os.path.join(self.target_folder, sn)
        if not os.path.isdir(current_path):
            os.makedirs(current_path)
        return current_path

    def getDti(self):
        dti = "None"
        dti_file = self.configInfo["DTI Read"]["file name"]
        dit_path = self.configInfo["DTI Read"]["file path"]
        dti_rule = self.configInfo["DTI Read"]["read rule"]
        for i in file_read(os.path.join(dit_path, dti_file)):
            print(i)
            tmp = re.findall(dti_rule, str(i))
            if len(tmp) > 0:
                dti = tmp[0]
                break
        return dti

    def get_gOS_files(self, sn):
        target = self.create(sn)
        files = self.configInfo["gOS Files"].items()
        for i in files:
            if i[1] is True:
                shell(self.copy_cmd % (i[0], target))

    def get_MacOS_files(self, sn):
        target = self.create(sn)
        files = self.configInfo["MacOS Files"]
        for i in files:
            copy(i, target)

    def special(self):
        serial_number = self.getSn()
        dti_info = self.getDti()
        self.get_gOS_files(serial_number)
        self.get_MacOS_files(serial_number)
        requests = self.configInfo["Special Request"]
        failures = os.path.join(self.create(serial_number), "failures.csv")

        rack_id = False
        for i in file_read(failures):
            tmp = str(i).split(",")
            for j in requests:
                if str(j) in tmp[1]:
                    rack_id = True
                    break
        return serial_number, dti_info, rack_id, self.create(serial_number)


def write_observation(serial_number=None, dti_info=None, path_road=None, rack_id=None):
    result = [
        ["Serial Number", "DTI Info", "Rack ID", "Get Time"],
        [str(serial_number), str(dti_info), str(rack_id), time.strftime("%Y-%m-%d %H:%M:%S")]
    ]
    pathRoad = os.path.join(path_road, "unit_info.csv")
    if os.path.isfile(pathRoad):
        os.remove(pathRoad)
    write_csv(result, pathRoad)
