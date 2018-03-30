#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time     : 2018/3/15下午3:09
# @Author   : Saseny Zhou
# @Site     : 
# @File     : yield_report.py
# @Software : PyCharm

from Functions.observation import *


class YieldReport():
    def __init__(self, configInfo):
        self.configInfo = configInfo["process"]
        if self.configInfo["Log Path"]["default"] is True:
            self.target_folder = resources
        else:
            self.target_folder = self.configInfo["Log Path"]["set path"]
        self.readFailure = Observation(configInfo)

    def ready(self, unitsInfo):
        serial_number = self.readFailure.getSn()
        if unitsInfo.get(serial_number, False) is not False:
            number = "#" + str(unitsInfo[serial_number]["number"]) + "_"
        else:
            number = ""
        newFolderName = number + serial_number
        folderPath = self.readFailure.create(newFolderName)
        dti_info = self.readFailure.getDti()
        id = "None"
        self.readFailure.get_gOS_files(newFolderName)
        write_observation(serial_number=serial_number, dti_info=dti_info, path_road=folderPath, rack_id=id)
        return folderPath, serial_number, dti_info

    def compare(self, unitsInfo, errorInfo):
        config = self.configInfo["failure read"]
        nameInt = config["combination"]["name"]
        statesInt = config["combination"]["states"]
        remove = config["replace"]

        folderPath, serial_number, dti_info = self.ready(unitsInfo)
        failures = file_read(os.path.join(folderPath, "failures.csv"))

        existCode = []
        needAdd = []
        exception = False

        for i in failures:
            tmp = str(i).split(",")
            if re.findall(r'^[A-Z]+$', tmp[0]):
                tmp_result = str(tmp[nameInt]).replace(remove, "") + " (Exit code: " + str(tmp[statesInt]) + ")"
                if errorInfo.get(tmp_result, False) is not False:
                    existCode.append(errorInfo[tmp_result])
                else:
                    needAdd.append((tmp_result))
                if exception is False:
                    exception = exception_check(self.configInfo, tmp_result)

        return_info = {
            "serial number": serial_number,
            "dti info": dti_info,
            "exist code": existCode,
            "need add": needAdd,
            "folder": folderPath,
            "exception": exception
        }
        return return_info


def exception_check(config, item):
    default = config["exception"]["default"]
    exception_list = config["exception"]["list"]

    if default is True:
        if str(item) not in exception_list:
            return True
    return False
