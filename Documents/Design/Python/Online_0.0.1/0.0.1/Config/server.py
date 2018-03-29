#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time     : 2018/3/29下午1:57
# @Author   : Saseny Zhou
# @Site     : 
# @File     : server.py
# @Software : PyCharm


serviceDict = {
    'DRUID': {
        'service': 'analysis/service/v1/metrics',
        'method': 'POST',
        'samplePayload': """{"toDate": "2017-12-10T02:59:59", "dimensions": ["equipmentType", "productCode", "siteName"], "summaryMetrics": ["appleYield"], "metrics": ["appleYield"], "fromDate": "2017-12-10T00:00:00", "filters": {"siteName": ["FXGL", "FXZZ", "PGPD", "PGKS", "WIKS"], "productCode": ["D20", "D201", "D21", "D211", "D22", "D221"]}, "granularity": "all"}"""
    },
    'MDM': {
        'service': 'mdm-common/service/v1/masterdata',
        'method': 'POST',
        'samplePayload': """{"type":"stationType","responseParams":["productCode","buildStep","stationType","siteName","includeInCumulativeYield","areaDisplayName","displayName"],"filterParams":{"productCode":{"operator":"AND","valueList":["D20"]},"yieldPoint":{"operator":"AND","valueList":["1"]},"siteName":{"valueList":["FXZZ"]}},"groupByParams":["productCode","stationType","siteName"]}"""
    },
    'GETMODULES': {
        'service': 'integrationservices.api/v1/getModules',
        'method': 'POST',
        'samplePayload': """{"serialNumber":  ["FK1VXKA3HFLR","FK1VXKL4HFLR","FK1VXKR1HFLR","FK1VXKVVHFLR","FK1VXNN0HFLR","FK1VXNZXHFLR","FK1VXQJVHFLR","FK1VXQLPHFLR","FK1VXTAGHFLR"] ,"options": {"allModules": true,"allModulesMaxLevel": 1,"includeDetails":"True","excludeMLB":"True"}}"""
    },
    'GETATTRIBUTES': {
        'service': 'integrationservices.api/v1/getAttributes',
        'method': 'POST',
        'samplePayload': """{"serialNumber": ["FK1VXKA3HFLR"],"options": {}}"""
    },
    'GETPARAMETRIC': {
        'service': 'integrationservices.api/v1/getParametric',
        'method': 'POST',
        'samplePayload': """{"serialNumber":["FK1VX396GRYK"],"stationType":["QT0"]}"""
    },
    'GETTESTS': {
        'service': 'integrationservices.api/v1/getTests',
        'method': 'POST',
        'samplePayload': """{"serialNumber": ["FK1VX396GRYK"]}"""
    },
    'FAILURE-SYMPTOMS': {
        'service': 'metrics.common/service/v1/failure-symptoms',
        'method': 'POST',
        'samplePayload': """{"equipmentType":["SHIPPING-SETTINGS"],"siteName":["FXBZ"],"productCode":["D20"],"fromDate":"2017-11-02T19:30:45","toDate":"2017-11-02T19:37:45"}"""
    },
    'POPULATION': {
        'service': 'integrationservices.api/v1/population',
        'method': 'POST',
        'samplePayload': """{"productCode":["N71"],"site":["FXZZ"], "stationType":["WIFI-BT-OTA"],"startTime":"2018-01-03 02:18:07" ,"endTime":"2018-01-03 02:30:07"}"""
    },
    'PFA': {
        'PARAMETRIC-SUBMIT': {
            'service': 'integrationservices.api/v1/submit-parametric-export',
            'method': 'POST',
            'samplePayload': ''
        },
        'PARAMETRIC-STATUS': {
            'service': 'integrationservices.api/v1/task/<TASKID>',
            'method': 'GET'
        },
        'PARAMETRIC-DOWNLOAD': {
            'service': 'export/service/v1/download/<TASKID>/stationType/<STATIONTYPE>',
            'method': 'GET'
        }
    }
}

from Path.path import *


def writer_service():
    write_json_file(serviceDict, os.path.join(resources, "service.json"))
