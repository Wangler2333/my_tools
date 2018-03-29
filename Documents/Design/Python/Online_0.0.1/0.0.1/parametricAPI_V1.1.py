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

url = 'https://manufacturing.apple.com/'

token = 'MOPTOKEN2a0d82c9e932ee77327c0f60a642e3cb875aa1523f5b4fa33f184c51dcedbbdb'  #Mop_session_id, change every 6 hours


serviceDict={
	'DRUID':{
		'service':'analysis/service/v1/metrics',
		'method':'POST',
		'samplePayload':"""{"toDate": "2017-12-10T02:59:59", "dimensions": ["equipmentType", "productCode", "siteName"], "summaryMetrics": ["appleYield"], "metrics": ["appleYield"], "fromDate": "2017-12-10T00:00:00", "filters": {"siteName": ["FXGL", "FXZZ", "PGPD", "PGKS", "WIKS"], "productCode": ["D20", "D201", "D21", "D211", "D22", "D221"]}, "granularity": "all"}"""
		},
	'MDM':{
		'service':'mdm-common/service/v1/masterdata',
		'method':'POST',
		'samplePayload':"""{"type":"stationType","responseParams":["productCode","buildStep","stationType","siteName","includeInCumulativeYield","areaDisplayName","displayName"],"filterParams":{"productCode":{"operator":"AND","valueList":["D20"]},"yieldPoint":{"operator":"AND","valueList":["1"]},"siteName":{"valueList":["FXZZ"]}},"groupByParams":["productCode","stationType","siteName"]}"""
		},
	'GETMODULES':{
		'service':'integrationservices.api/v1/getModules',
		'method':'POST',
		'samplePayload':"""{"serialNumber":  ["FK1VXKA3HFLR","FK1VXKL4HFLR","FK1VXKR1HFLR","FK1VXKVVHFLR","FK1VXNN0HFLR","FK1VXNZXHFLR","FK1VXQJVHFLR","FK1VXQLPHFLR","FK1VXTAGHFLR"] ,"options": {"allModules": true,"allModulesMaxLevel": 1,"includeDetails":"True","excludeMLB":"True"}}"""
	},
	'GETATTRIBUTES':{
		'service':'integrationservices.api/v1/getAttributes',
		'method':'POST',
		'samplePayload':"""{"serialNumber": ["FK1VXKA3HFLR"],"options": {}}"""
	},
	'GETPARAMETRIC':{
		'service':'integrationservices.api/v1/getParametric',
		'method':'POST',
		'samplePayload':"""{"serialNumber":["FK1VX396GRYK"],"stationType":["QT0"]}"""
	},
	'GETTESTS':{
		'service':'integrationservices.api/v1/getTests',
		'method':'POST',
		'samplePayload':"""{"serialNumber": ["FK1VX396GRYK"]}"""
	},
	'FAILURE-SYMPTOMS':{
		'service':'metrics.common/service/v1/failure-symptoms',
		'method':'POST',
		'samplePayload':"""{"equipmentType":["SHIPPING-SETTINGS"],"siteName":["FXBZ"],"productCode":["D20"],"fromDate":"2017-11-02T19:30:45","toDate":"2017-11-02T19:37:45"}"""
	},
	'POPULATION':{
		'service':'integrationservices.api/v1/population',
		'method':'POST',
		'samplePayload':"""{"productCode":["N71"],"site":["FXZZ"], "stationType":["WIFI-BT-OTA"],"startTime":"2018-01-03 02:18:07" ,"endTime":"2018-01-03 02:30:07"}"""
	},
	'PFA':{
		'PARAMETRIC-SUBMIT':{
			'service':'integrationservices.api/v1/submit-parametric-export',
			'method':'POST',
			'samplePayload':''
			},
		'PARAMETRIC-STATUS':{
			'service':'integrationservices.api/v1/task/<TASKID>',
			'method':'GET'
			},
		'PARAMETRIC-DOWNLOAD':{
			'service':'export/service/v1/download/<TASKID>/stationType/<STATIONTYPE>',
			'method':'GET'
			}
		}
}

headers = {'Content-Type': 'application/json','Accept':'application/json','mop_session_id':token}



def parametricSubmit(parameterDict=''):
	start = datetime.datetime.now()

	API_TYPE = 'PARAMETRIC-SUBMIT'
	fullUrl = url + serviceDict['PFA'][API_TYPE]['service']
	headers = {'Content-Type': 'application/json','Accept':'application/json','mop_session_id':token}
	payload = parameterDict

	if type(payload) !=str:
		payload = json.dumps(payload)
	response = requests.post(fullUrl, data=payload, headers=headers)
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
	Finish: %s""" % (start.strftime('%Y-%m-%s %H:%M:%S'),end.strftime('%Y-%m-%s %H:%M:%S'),str((end-start).total_seconds()))

	return response


def parametricStatus(taskID):

	API_TYPE = 'PARAMETRIC-STATUS'
	fullUrl = url + serviceDict['PFA'][API_TYPE]['service']
	fullUrl = fullUrl.replace('<TASKID>',str(int(taskID)))
	headers = {'Content-Type': 'application/json','Accept':'application/json','mop_session_id':token}

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
	
def parametricDownloadFile(local_filename,taskID,stationType):
	API_TYPE = 'PARAMETRIC-DOWNLOAD'
	fullUrl = url + serviceDict['PFA'][API_TYPE]['service']
	fullUrl = fullUrl.replace('<TASKID>',str(int(taskID))).replace('<STATIONTYPE>',stationType)

	headers = {'Content-Type': 'application/json','Accept':'application/json','mop_session_id':token}


	r = requests.get(fullUrl,headers=headers,stream=True)
	# local_filename='test.gz'

	with open(local_filename, 'wb') as f:
		for chunk in r.iter_content(chunk_size=1024):
			if chunk: # filter out keep-alive new chunks
				f.write(chunk)

	return local_filename
	


def parametricDownload(filename,taskID,stationList,sleepSeconds=30,maxTimeInMin=60,wait=True):
	start = datetime.datetime.now()
	taskResponse =0
	counter=0
	while taskResponse != 7 or counter>maxTimeInMin/sleepSeconds:
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
			#print taskResponse
			if taskResponse==7:
				break
		if not wait:
			break
		time.sleep(sleepSeconds)
		counter=counter+1

	end = datetime.datetime.now()
	print """parametric queue finish
	Start: %s
	End: %s
	Finish: %s""" % (start.strftime('%Y-%m-%s %H:%M:%S'),end.strftime('%Y-%m-%s %H:%M:%S'),str((end-start).total_seconds()))


	start = datetime.datetime.now()
	if taskResponse ==7:
		filename = parametricDownloadFile(filename,taskID,stationList)
		end = datetime.datetime.now()
		print """parametric download finish
	Start: %s
	End: %s
	Finish: %s""" % (start.strftime('%Y-%m-%s %H:%M:%S'),end.strftime('%Y-%m-%s %H:%M:%S'),str((end-start).total_seconds()))

	if counter >(maxTimeInMin*60)/sleepSeconds:
		print 'Process Took longer than {} minutes so was killed'.format(maxTimeInMin)
	
	return filename,taskResponse


if __name__ =="__main__":

	#Insight API - Run Parametric Export API Request
	payload = {}
	payload['siteName'] =['PGKS']
	payload['parametricType'] = []

	parametricType = {}
	parametricType['stationType'] = "ALS-CAL"
	parametricType['overlayVerion'] = []
	parametricType['limitsVersion'] = []
	parametricType['selectAll'] = True
	payload['parametricType'].append(parametricType)

	#Can take in multipe station types, Uncomment to add second station QT0
	#parametricType = {}
	#parametricType['stationType'] = "QT0"
	#parametricType['overlayVerion'] = []
	#parametricType['limitsVersion'] = []
	#parametricType['selectAll'] = True
	#payload['parametricType'].append(parametricType)

	payload['dataCategory'] = ["pdata"]
	payload['requestedColumns'] = ["siteName","productCode","serialNumber","specialBuildName","specialBuildDescription","unitNumber","stationId","testResult","startTestTime","endTestTime","overlayVersion","listOfFailingTests"]
	payload['testCategory'] = ["All"]
	payload['passFailCategory'] = ["All"]
	payload["nullIncluded"] = "Y"
	payload["samplePercent"] = "100"
	payload["startTime"] = "2018-01-27 00:00:00"
	payload["endTime"] = "2018-01-29 00:00:00"
	payload["frequency"] = "now"
	payload['productCode'] = ["D20"]
	refreshData=True
	print payload
	#Get station list from request to be used later for extraction
	stationList =[]
	for i,item in enumerate(payload['parametricType']):
	    stationList.append(item['stationType'])
	if refreshData:
	    #response=ins.parametricSubmit(parameterDict=payload)
	    response=parametricSubmit(parameterDict=payload)
	    jsonResponse = response.json()
	    print jsonResponse
	    taskID, statusCode = jsonResponse['exportResponse']['taskId'], jsonResponse['statusCode']
	    print taskID, statusCode


	#Insight API - Retrieve ParametricData
	filename = 'test.gz'
	#taskID ='27252' # Comment this out to pull taskID created from previous step
	# stationList = ['ALS-CAL']
	# If file is ready parametricDownload will download the file to filename
	# If file is not ready and wait=True function will wait on file to complete on Insight, then download
	# If file is not ready and wait=False function will return its current file status on Insight
	filename = parametricDownload(filename,taskID,stationList[0],wait=True)



