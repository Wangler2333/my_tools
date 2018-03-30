#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time     : 2018/2/21下午7:32
# @Author   : Saseny Zhou
# @Site     : 
# @File     : plot.py
# @Software : PyCharm


payload_dict = {
    "siteName": ["QSMC"],
    "auditOnly": "Y",
    "parametricType": [
        {
            "stationType": "null",
            "overlayVersion": ["null"],
            "limitsVersion": [],
            "selectAll": True
        }
    ],
    "dataCategory": ["pdata"],
    "requestedColumns":
        ["siteName", "productCode", "serialNumber", "specialBuildName", "specialBuildDescription", "unitNumber",
         "stationId", "testResult", "startTestTime", "endTestTime", "overlayVersion", "listOfFailingTests"],
    "testCategory": ["All"],
    "passFailCategory": ["All"],
    "nullIncluded": "N",
    "samplePercent": "100",
    "startTime": "null",
    "endTime": "null",
    "frequency": "now",
    "productCode": ["null"]
}

"""
null :  需要在运行过程中添加的参数
"""

from functions.path import *
from functions.json_file import *

payload_path_road = os.path.join(resources, "payload.json")


def writer_define_payload():
    write_json_file(payload_dict, payload_path_road)


def time_change(times):
    time_array = time.localtime(times)
    return time.strftime("%Y-%m-%d %H:%M:%S", time_array)


def payload_parameter(args):
    endDate = time.strftime("%Y-%m-%d %H:%M:%S")
    startDate = time_change(int(time.time()) - 86400 * int(args["download"]["form_start_time"]))

    return_dict = read_json_file(payload_path_road)
    if return_dict is not False:
        return_dict["parametricType"][0]["stationType"] = args["download"]["station"]
        return_dict["parametricType"][0]["overlayVersion"] = []
        return_dict["auditOnly"] = args["download"]["auditOnly"]  # auditOnly follow main config set-up
        return_dict["productCode"] = []
        return_dict["startTime"] = startDate
        return_dict["endTime"] = endDate

        if type(args["download"]["overlay"]) is str:
            return_dict["parametricType"][0]["overlayVersion"].append(args["download"]["overlay"])
        elif type(args["download"]["overlay"]) is list:
            return_dict["parametricType"][0]["overlayVersion"] = args["download"]["overlay"]

        if type(args["download"]["project"]) is str:
            return_dict["productCode"].append(args["download"]["project"])
        elif type(args["download"]["project"]) is list:
            return_dict["productCode"] = args["download"]["project"]

        return return_dict
    else:
        writer_define_payload()
        payload_parameter(args=args)
