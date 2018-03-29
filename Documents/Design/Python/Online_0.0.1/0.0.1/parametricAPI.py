#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import sys
import pandas as pd
import requests
import json
from operator import itemgetter
import datetime
import subprocess
import math
import pytz
import re
import csv
from decimal import *
import math
import time
import json

import multiprocessing as mp
from multiprocessing import Process, Queue, Manager
from requests.packages.urllib3.fields import RequestField
from requests.packages.urllib3.filepost import encode_multipart_formdata

url = 'https://manufacturing.apple.com/'

global token
token = 'MOPTOKENf27a4d03d1b65ae2b60e3f95c75e3d09d70a89ea49b52fa92f8e42fa9342b2b3'

serviceDict = {
    'DRUID': {
        'service': 'analysis/service/v1/metrics',
        'method': 'POST',
        'samplePayload': """{"toDate": "2018-02-07T00:59:59", "dimensions": ["equipmentType", "siteName", "productCode", "lineName", "serialNumber"], "summaryMetrics": ["appleYield"], "metrics": ["appleYield"], "fromDate": "2018-02-07T00:00:00", "filters": {"siteName": ["WIKS"], "productCode": ["D21"], "equipmentType": ["ALS-CAL"]}, "granularity": "all"}"""
    },
    'MDM': {
        'service': 'mdm-common/service/v1/masterdata',
        'method': 'POST',
        'samplePayload': """{"type":"stationType","responseParams":["productCode","buildStep","stationType","siteName","includeInCumulativeYield","areaDisplayName","displayName"],"filterParams":{"productCode":{"operator":"AND","valueList":["D20"]},"yieldPoint":{"operator":"AND","valueList":["1"]},"siteName":{"valueList":["FXZZ"]}},"groupByParams":["productCode","stationType","siteName"]}"""
    },
    'GETMODULES': {
        'service': 'integrationservices.api/v1/getModules',
        'method': 'POST',
        'samplePayload': """{"serialNumber":  ["FK1VXKA3HFLR","FK1VXKL4HFLR","FK1VXKR1HFLR","FK1VXKVVHFLR","FK1VXNN0HFLR","FK1VXNZXHFLR","FK1VXQJVHFLR","FK1VXQLPHFLR","FK1VXTAGHFLR"] ,"options": {"allModules": "False","allModulesMaxLevel": 1,"includeDetails":"True","excludeMLB":"True"},"type":["CGS"]}"""
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
    'GETSERIALNUMBERINFORMATION': {
        'service': 'lookupservices/v1/getSerialNumberInformation',
        'method': 'POST',
        'samplePayload': """{"filters":{"siteName":["FXGL"],"productCode":["D22"],"syResultType":["FAIL"],"equipmentType":["QT0"]},"additionalInfo":{},"fromDate":"2017-12-02T04:00:00+08:00","toDate":"2017-12-02T04:29:59+08:00"}"""
    },
    'FAILURE-SYMPTOMS': {
        'service': 'metrics.common/service/v1/failure-symptoms',
        'method': 'POST',
        'samplePayload': """{"equipmentType":["SHIPPING-SETTINGS"],"siteName":["FXBZ"],"productCode":["D20"],"fromDate":"2017-11-02T19:30:45","toDate":"2017-11-02T19:37:45"}"""
    },
    'POPULATION': {
        'service': 'integrationservices.api/v1/unit-population',
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

headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'mop_session_id': token}


def callAPIfromDict(parameterDict, serviceType, headers=headers):
    fullUrl = url + serviceDict[serviceType]['service']

    headers['mop_session_id'] = token
    # print str(headers)
    if type(parameterDict) == type('abcd'):
        payload = parameterDict
    else:
        payload = json.dumps(parameterDict)
    print str(payload)[:300]

    r = requests.post(fullUrl, data=payload, headers=headers)
    # requests.get(fullUrl,headers=headers)

    return r


def executeAPIandRetry(executionFunction, serviceType, parameterDict, return_key=1, return_dict={}, retryLimit=5):
    print '%s STARTING %s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), str(return_key))
    for i in range(0, retryLimit):
        response = executionFunction(parameterDict, serviceType)

        # 204 No Data Found
        if response.status_code == 204:
            print  "No Data Found For"
            print str(parameterDict)
            jsonResponse = ''
            print '%s FINISH REQUEST %s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), str(return_key))
            break

        jsonResponse = response.json()

        # if tokenmanager.reToken(jsonResponse):
        # 	global token
        # 	print str(token)
        # 	token = tokenmanager.tokenUp()
        # 	print str(token)

        if jsonResponse['statusCode'] == "200":
            print "REQUEST COMPLETED"
            break
        elif jsonResponse['statusCode'] == "403":
            # send message when this happens
            print  jsonResponse['statusCode'] + jsonResponse['statusMessage']
            break
        else:
            # send message when this happens
            print  jsonResponse['statusCode'] + str(jsonResponse)
        time.sleep(5)

    parameterDict = json.dumps(parameterDict)
    if return_dict == {}:
        print jsonResponse['statusCode'] + str(jsonResponse)[:100]
        return response, jsonResponse
    print '%s RETURNING JSON RESPONSE %s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), str(return_key))
    return_dict[return_key] = {'response': response, 'jsonResponse': jsonResponse}


# return response, jsonResponse
# return


def convertResponseToDF(serviceType, jsonResponse, return_dict={}, key=1):
    if serviceType == 'DRUID':
        df = pd.DataFrame()

        metrics = jsonResponse['granularMetricsView']
        finalFile = []
        for key, value in metrics.iteritems():
            for item in value:
                if item['appleYieldRowCount'] != 0:
                    item['testDate'] = key[:10] + ' ' + key[11:19]
                    finalFile.append(item)
        df = pd.DataFrame(finalFile)

    elif serviceType == "GETSERIALNUMBERINFORMATION":
        df = pd.DataFrame()
        metrics = jsonResponse['serilaNumberInfo']
        # print "START ITERDUMP %s" % (datetime.datetime.now())
        # for metric in metrics:
        # 	df.append(pd.DataFrame([metric]))
        # print "FINISH ITERDUMP %s" % (datetime.datetime.now())

        print "START FULLDUMP %s" % (datetime.datetime.now())
        df = pd.DataFrame(metrics)
        print "FINISH FULLDUMP %s" % (datetime.datetime.now())



    elif serviceType == 'GETTESTS':
        testTable = []
        try:
            tests = jsonResponse['data']
            df = pd.DataFrame(tests)
        except KeyError:
            tests = []
            df = pd.DataFrame()

    # for test in tests:
    # 	serialNumber = test['serialNumber']
    # 	if test['tests']:
    # 		for record in test['tests']:
    # 			record['processLogs'] = ''
    # 			record['serialNumber'] = serialNumber
    # 			if "startTime" not in record:
    # 				record['startTime'] = '0000-00-00 00:00:00'
    # 			if "endTime" not in record:
    # 				record['endTime'] = '0000-00-00 00:00:00'
    # 			testTable.append(record)
    # 	else:
    # 		record={}
    # 		record['serialNumber'] = serialNumber
    # 		testTable.append(record)

    elif serviceType == 'GETMODULES':
        moduleTable = []
        try:
            modules = jsonResponse['data']
        except KeyError:
            modules = []

        for module in modules:
            for record in module['modules']:
                record['unitSerialNumber'] = module['serialNumber']
                if "allTime" not in record:
                    record['allTime'] = '0000-00-00 00:00:00'
                    if "serialNumber" not in record:
                        record['serialNumber'] = ''
                moduleTable.append(record)

        newlist = sorted(moduleTable, key=itemgetter('unitSerialNumber', 'type', 'allTime'))

        for i, item in enumerate(newlist):

            if i < len(newlist) - 1:
                if item['type'] != newlist[i + 1]['type'] and item['recordType'] == 'ADD':
                    newlist[i]['alled'] = 'YES'
                else:
                    newlist[i]['alled'] = 'NO'
            # Check for last module in list
            if i == len(newlist) - 1 and item['recordType'] == 'ADD':
                newlist[i]['alled'] = 'YES'

        for i, item in enumerate(newlist):
            pass
        # print "{} - {} - {} - {} - {} - {} ".format(item['unitSerialNumber'],item['type'],item['serialNumber'],item['allTime'],item['recordType'],item['alled'])

        df = pd.DataFrame(newlist, index=None)

    elif serviceType == 'GETATTRIBUTES':
        attributeTable = []
        try:
            snList = jsonResponse['data']
            df = pd.DataFrame(snList)
        except KeyError:
            attributes = []
            df = pd.DataFrame()

    # for snRecord in snList:
    # 	for record in snRecord['attributes']:
    # 		record['serialNumber'] = snRecord['serialNumber']
    # 		if "timestamp" not in record:
    # 			record['timestamp'] = '0000-00-00 00:00:00'
    # 		attributeTable.append(record)

    # # df = pd.DataFrame(attributeTable,index=None)

    elif serviceType == 'POPULATION':
        snTable = []
        try:
            snList = jsonResponse['data']
        except KeyError:
            snList = []

        for snRecord in snList:
            snTable.append(snRecord)

        df = pd.DataFrame(snTable, index=None)

    if return_dict == {}:
        return df
    return_dict[key] = {'df': df}
    return


def fillEmptyDF(serviceType, parameterDict):
    print  'Using placeholder and input payload to populate schema'
    fullUrl = url + serviceDict[serviceType]['service']
    samplePayload = json.loads(serviceDict[serviceType]['samplePayload'])
    emptyDict = parameterDict.copy()
    # DRUID
    if serviceType == 'DRUID':
        emptyDict['toDate'] = samplePayload['toDate']
        emptyDict['fromDate'] = samplePayload['fromDate']
        emptyDict['filters'] = samplePayload['filters']

    # executableFunction= getMetricsAPI

    # elif serviceType == ''

    else:  # serviceType in ['GETTESTS','GETATTRIBUTES','GETMODULES']
        emptyDict = samplePayload

        try:  # removing attributeName filter for getAttributes
            emptyDict.pop('attributeName')
        except KeyError:
            pass
        try:  # removing moduleType filter from getModules
            emptyDict.pop('type')
        except KeyError:
            pass
        try:  # removing stationType filter from stationType
            emptyDict.pop('stationType')
        except KeyError:
            pass

    response, jsonResponse = executeAPIandRetry(callAPIfromDict, serviceType, emptyDict)

    if response.status_code == 204:
        smallDF = pd.DataFrame()
    # Need to alert that fills are no longer working

    df = convertResponseToDF(serviceType, jsonResponse)

    return df.iloc[0:0]


def getMetricsToDF(parameterDict, processes=2, maxtasksperchild=50):
    print 'Running getMetricsToDF'

    serviceType = 'DRUID'

    fromDate = parameterDict['fromDate']
    toDate = parameterDict['toDate']

    df = fillEmptyDF('DRUID', parameterDict)

    fromDateObj = datetime.datetime.strptime(fromDate, '%Y-%m-%d %H:%M:%S')
    toDateObj = datetime.datetime.strptime(toDate, '%Y-%m-%d %H:%M:%S')

    if int((((toDateObj - fromDateObj).total_seconds()) / 86400)) == (toDateObj - fromDateObj).total_seconds() / 86400:
        dayDelta = int((((toDateObj - fromDateObj).total_seconds()) / 86400))
    else:
        dayDelta = int((((toDateObj - fromDateObj).total_seconds()) / 86400) + 1)
    dayAdder = datetime.timedelta(days=1)

    q = Manager()
    return_dict = q.dict()
    jobs = []
    payload = {}
    pool = mp.Pool(processes=processes, maxtasksperchild=maxtasksperchild)
    counter = 1
    for i in range(0, dayDelta):
        fromDate = fromDateObj.strftime('%Y-%m-%dT%H:%M:%S')
        toDate = min(fromDateObj.strftime('%Y-%m-%dT23:59:59'), toDateObj.strftime('%Y-%m-%dT%H:%M:%S'))
        bufferToDate = datetime.datetime.strptime(toDate, '%Y-%m-%dT%H:%M:%S')
        if bufferToDate.second == 0:
            minusSecond = datetime.timedelta(seconds=1)
            toDate = (bufferToDate - minusSecond).strftime('%Y-%m-%dT%H:%M:%S')

        # toDate = fromDateObj.strftime('%Y-%m-%dT23:59:59')
        parameterDict['fromDate'] = fromDate
        parameterDict['toDate'] = toDate
        iterDict = json.dumps(parameterDict)
        # Retry method for catching status_code 500
        task = pool.apply_async(executeAPIandRetry, (callAPIfromDict, serviceType, iterDict, counter, return_dict))
        counter = counter + 1
        fromDateObj = fromDateObj + dayAdder
        fromDateObj = datetime.datetime(fromDateObj.year, fromDateObj.month, fromDateObj.day)
    # response, jsonResponse = executeAPIandRetry(callAPIfromDict,serviceType,parameterDict)
    pool.close()
    pool.join()

    return_dict2 = q.dict()
    pool = mp.Pool(processes=processes, maxtasksperchild=maxtasksperchild)

    for key in return_dict.keys():

        if return_dict[key]['jsonResponse'] == '' or return_dict[key]['response'].status_code == 204:
            smallDF = pd.DataFrame()
        else:
            task = pool.apply_async(convertResponseToDF,
                                    (serviceType, return_dict[key]['jsonResponse'], return_dict2, key))

    pool.close()
    pool.join()

    for key in return_dict2.keys():
        df = df.append(return_dict2[key]['df'])

    floatList = ["appleYieldRowCount", "appleYieldFailCount", "appleYieldPassCount", "appleYieldRetestCount",
                 "systemYieldRowCount", "systemYieldFailCount", "systemYieldPassCount", "systemYieldRetestCount"]
    floatDict = {}
    for item in floatList:
        if item in list(df.columns):
            floatDict[item] = float
    try:
        snList = list(df['serialNumber'].unique())
    except KeyError:
        snList = []
    return df, snList


def parametricSubmit(parameterDict=''):
    start = datetime.datetime.now()

    API_TYPE = 'PARAMETRIC-SUBMIT'
    fullUrl = url + serviceDict['PFA'][API_TYPE]['service']
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'mop_session_id': token}
    payload = parameterDict

    if type(payload) != str:
        payload = json.dumps(payload).replace("'", '"')
    response = requests.post(fullUrl, data=payload, headers=headers)
    print payload
    print fullUrl

    jsonResponse = response.json()

    # if tokenManager.reToken(jsonResponse):
    # 	global token
    # 	token=tokenManager.tokenUp()
    # 	headers['mop_session_id']=token
    # 	response = requests.post(fullUrl, data=payload, headers=headers)

    end = datetime.datetime.now()

    print """parametricSubmit
	Start: %s
	End: %s
	Finish: %s""" % (
        start.strftime('%Y-%m-%s %H:%M:%S'), end.strftime('%Y-%m-%s %H:%M:%S'), str((end - start).total_seconds()))

    return response


def parametricStatus(taskID):
    API_TYPE = 'PARAMETRIC-STATUS'
    fullUrl = url + serviceDict['PFA'][API_TYPE]['service']
    fullUrl = fullUrl.replace('<TASKID>', str(int(taskID)))
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'mop_session_id': token}

    r = requests.get(fullUrl, headers=headers)

    return r


def decodeParametricStatus(taskStatus):
    if taskStatus == 1:
        print 'TASK HAS QUEUED'
    elif taskStatus == 2:
        print 'TASK HAS BEEN SUBMITTED FOR PROCESSING'
    elif taskStatus == 3:
        print 'TASK HAS BEEN SUBMITTED'
    elif taskStatus == 4:
        print 'EXPORTS IN PROCESS OF GENERATION'
    elif taskStatus == 5:
        print 'EXPORTS FINISHED GENERATION'
    elif taskStatus == 6:
        print 'TASK FAILED'
    elif taskStatus == 7:
        print 'EXPORTS READY'
    elif taskStatus == 8:
        print 'TASK HAD AN ERROR AND NOTIFICATION HAS BEEN SENT'
    elif taskStatus == 9:
        print 'EXPORTS HAVE BEEN DOWNLOADED'
    elif taskStatus == 10:
        print 'TASK TIMEOUT'
    elif taskStatus == 11:
        print 'ERROR OCCURED WHILE MONITORING STATUS'
    elif taskStatus == 21:
        print 'TASK STATUS SUBMITTED TO SPARK -- for META DATA'
    else:
        print 'UNDOCUMENTED RETURN %s' % (str(taskStatus))

    return taskStatus


def parametricDownloadFile(local_filename, taskID, stationType):
    API_TYPE = 'PARAMETRIC-DOWNLOAD'
    fullUrl = url + serviceDict['PFA'][API_TYPE]['service']
    fullUrl = fullUrl.replace('<TASKID>', str(int(taskID))).replace('<STATIONTYPE>', stationType)

    headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'mop_session_id': token}

    r = requests.get(fullUrl, headers=headers, stream=True)
    # local_filename='test.gz'

    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)

    return local_filename


def parametricDownload(filename, taskID, stationList, sleepSeconds=30, maxTimeInMin=60, wait=True):
    start = datetime.datetime.now()
    taskResponse = 0
    counter = 0
    while taskResponse != 7 or counter > maxTimeInMin / sleepSeconds:
        response = parametricStatus(taskID)
        jsonResponse = response.json()
        # print jsonResponse
        # if tokenManager.reToken(jsonResponse):
        # 	global token
        # 	token=tokenManager.tokenUp()
        # 	headers['mop_session_id']=token
        # 	response = parametricStatus(taskID)
        # 	jsonResponse = response.json()
        if response.status_code in [200]:
            taskResponse = decodeParametricStatus(jsonResponse['exportResponse']['taskStatus'])
            # print taskResponse
            if taskResponse == 7:
                break
        if not wait:
            break
        time.sleep(sleepSeconds)
        counter = counter + 1

    end = datetime.datetime.now()
    print """parametric queue finish
	Start: %s
	End: %s
	Finish: %s""" % (
        start.strftime('%Y-%m-%s %H:%M:%S'), end.strftime('%Y-%m-%s %H:%M:%S'), str((end - start).total_seconds()))

    start = datetime.datetime.now()
    if taskResponse == 7:
        filename = parametricDownloadFile(filename, taskID, stationList)
        end = datetime.datetime.now()
        print """parametric download finish
	Start: %s
	End: %s
	Finish: %s""" % (
            start.strftime('%Y-%m-%s %H:%M:%S'), end.strftime('%Y-%m-%s %H:%M:%S'), str((end - start).total_seconds()))

    if counter > (maxTimeInMin * 60) / sleepSeconds:
        print 'Process Took longer than {} minutes so was killed'.format(maxTimeInMin)

    return filename, taskResponse


if __name__ == "__main__":
    payload = {}
    startDate = """2018-01-31 00:00:00"""
    endDate = """2018-01-31 23:59:59"""
    # REQUIRED
    payload['fromDate'] = startDate
    payload['toDate'] = endDate
    payload[
        'granularity'] = "hour"  # all, none, second, minute, fifteen_minute, thirty_minute, hour, day, week, month, quarter and year
    payload["metrics"] = ["appleYield"]  # appleYield, systemYield

    # OPTIONAL
    payload["summaryMetrics"] = ["appleYield"]
    payload["dimensions"] = ["equipmentType", "siteName", "productCode", "lineName"]
    payload["filters"] = {}
    payload["filters"]["siteName"] = ['WIKS']
    payload["filters"]["productCode"] = ['D20', 'D201', 'D21', 'D211', 'D22', 'D221', 'D10', 'D101', 'D11', 'D111',
                                         'N71', 'N66']
    payload["filters"]["equipmentType"] = ["ALS-CAL"]

    metricsTable, metricsSerialList = getMetricsToDF(payload, processes=8, maxtasksperchild=50)

    print metricsTable

# if __name__ =="__main____":

# 	#Insight API - Run Parametric Export API Request
# 	payload = {}
# 	payload['siteName'] =['WIKS']
# 	payload['parametricType'] = []

# 	parametricType = {}
# 	parametricType['stationType'] = "ALS-CAL"
# 	parametricType['overlayVerion'] = []
# 	parametricType['limitsVersion'] = []
# 	parametricType['selectAll'] = True
# 	payload['parametricType'].append(parametricType)

# 	#Can take in multipe station types, Uncomment to add second station QT0
# 	#parametricType = {}
# 	#parametricType['stationType'] = "QT0"
# 	#parametricType['overlayVerion'] = []
# 	#parametricType['limitsVersion'] = []
# 	#parametricType['selectAll'] = True
# 	#payload['parametricType'].append(parametricType)

# 	payload['dataCategory'] = ["pdata"]
# 	payload['requestedColumns'] = ["siteName","productCode","serialNumber","specialBuildName","specialBuildDescription","unitNumber","stationId","testResult","startTestTime","endTestTime","overlayVersion","listOfFailingTests"]
# 	payload['testCategory'] = ["All"]
# 	payload['passFailCategory'] = ["All"]
# 	payload["nullIncluded"] = "Y"
# 	payload["samplePercent"] = "100"
# 	payload["startTime"]='2018-01-03 00:00:00'
# 	payload["endTime"]="2018-01-04 00:00:00"
# 	# payload["startTime"] = startDate
# 	# payload["endTime"] = endDate
# 	payload["frequency"] = "now"
# 	payload['productCode'] = ["D21","D211"]

# 	print payload
# 	#Get station list from request to be used later for extraction
# 	stationList =[]
# 	for i,item in enumerate(payload['parametricType']):
# 	    stationList.append(item['stationType'])
# # 	if refreshData:
# 	response=parametricSubmit(parameterDict=payload)
# 	jsonResponse = response.json()
# 	print jsonResponse
# 	taskID, statusCode = jsonResponse['exportResponse']['taskId'], jsonResponse['statusCode']


# 	#Insight API - Retrieve ParametricData
# 	filename = 'test.gz'
# 	#taskID ='27252' # Comment this out to pull taskID created from previous step
# 	# stationList = ['ALS-CAL']
# 	# If file is ready parametricDownload will download the file to filename
# 	# If file is not ready and wait=True function will wait on file to complete on Insight, then download
# 	# If file is not ready and wait=False function will return its current file status on Insight
# 	filename = parametricDownload(filename,taskID,stationList[0],wait=True)
