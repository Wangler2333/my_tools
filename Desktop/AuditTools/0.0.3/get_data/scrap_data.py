#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time     : 2018/2/7下午12:23
# @Author   : Saseny Zhou
# @Site     : 
# @File     : scrap_data.py
# @Software : PyCharm


import requests
import datetime
from config.plot import *


class Scrapy_Data():
    def __init__(self, main_config, server_config, tokenId):
        self.url = main_config["url"]
        self.serviceDict = server_config
        self.tokenID = tokenId

    def parametricSubmit(self, parameterDict):
        start = datetime.datetime.now()

        API_TYPE = "PARAMETRIC-SUBMIT"
        fullUrl = self.url + self.serviceDict["PFA"][API_TYPE]["service"]
        headers = {"Content-Type": "application/json", "Accept": "application/json", "mop_session_id": self.tokenID}
        payload = parameterDict

        print(fullUrl)
        print(headers)

        if type(payload) != str:
            payload = json.dumps(payload)
        response = requests.post(fullUrl, data=payload, headers=headers)

        jsonResponse = response.json()

        # if tokenManager.reToken(jsonResponse):
        # 	global token
        # 	token=tokenManager.tokenUp()
        # 	headers['mop_session_id']=token
        # 	response = requests.post(fullUrl, data=payload, headers=headers)

        end = datetime.datetime.now()

        print("""parametricSubmit
        Start: %s
        End: %s
        Finish: %s""" % (
            start.strftime("%Y-%m-%s %H:%M:%S"), end.strftime("%Y-%m-%s %H:%M:%S"), str((end - start).total_seconds())))

        return response

    def parametricStatus(self, taskID):
        API_TYPE = "PARAMETRIC-STATUS"
        fullUrl = self.url + self.serviceDict["PFA"][API_TYPE]["service"]
        fullUrl = fullUrl.replace("<TASKID>", str(int(taskID)))
        headers = {"Content-Type": "application/json", "Accept": "application/json", "mop_session_id": self.tokenID}
        r = requests.get(fullUrl, headers=headers)
        return r

    def decodeParametricStatus(self, taskStatus, states_json_path, stationList, taskID):
        if taskStatus == 1:
            message = "TASK HAS QUEUED"
        elif taskStatus == 2:
            message = "TASK HAS BEEN SUBMITTED FOR PROCESSING"
        elif taskStatus == 3:
            message = "TASK HAS BEEN SUBMITTED"
        elif taskStatus == 4:
            message = "EXPORTS IN PROCESS OF GENERATION"
        elif taskStatus == 5:
            message = "EXPORTS FINISHED GENERATION"
        elif taskStatus == 6:
            message = "TASK FAILED"
        elif taskStatus == 7:
            message = "EXPORTS READY"
        elif taskStatus == 8:
            message = "TASK HAD AN ERROR AND NOTIFICATION HAS BEEN SENT"
        elif taskStatus == 9:
            message = "EXPORTS HAVE BEEN DOWNLOADED"
        elif taskStatus == 10:
            message = "TASK TIMEOUT"
        elif taskStatus == 11:
            message = "ERROR OCCURED WHILE MONITORING STATUS"
        elif taskStatus == 21:
            message = "TASK STATUS SUBMITTED TO SPARK -- for META DATA"
        else:
            message = "UNDOCUMENTED RETURN %s" % str(taskStatus)

        dict_info = {
            "id": taskID,
            "taskStatus": taskStatus,
            "taskInfo": message,
            "station": stationList
        }
        final = os.path.join(states_json_path, str(stationList) + "_" + str(int(taskID)) + ".json")
        write_json_file(dict_info, final)
        print(dict_info)

        return taskStatus

    def parametricDownloadFile(self, local_filename, stationType, taskID):
        API_TYPE = "PARAMETRIC-DOWNLOAD"
        fullUrl = self.url + self.serviceDict["PFA"][API_TYPE]["service"]
        fullUrl = fullUrl.replace("<TASKID>", str(int(taskID))).replace("<STATIONTYPE>", stationType)
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'mop_session_id': self.tokenID}
        r = requests.get(fullUrl, headers=headers, stream=True)
        # local_filename='test.gz'

        print(fullUrl)
        print(headers)

        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)

        return local_filename

    def parametricDownload(self, filename, taskID, stationList, states_json_path, sleepSeconds=30, maxTimeInMin=60,
                           wait=True):
        start = datetime.datetime.now()
        taskResponse = 0
        counter = 0
        while taskResponse != 7 or counter > maxTimeInMin / sleepSeconds:
            response = self.parametricStatus(taskID)
            jsonResponse = response.json()
            if response.status_code in [200]:
                taskResponse = self.decodeParametricStatus(jsonResponse['exportResponse']['taskStatus'],
                                                           states_json_path, stationList, taskID)
                if taskResponse == 7:
                    break
            if not wait:
                break
            time.sleep(sleepSeconds)
            counter = counter + 1

        end = datetime.datetime.now()
        print("""parametric queue finish
    	Start: %s
    	End: %s
    	Finish: %s""" % (
            start.strftime('%Y-%m-%s %H:%M:%S'), end.strftime('%Y-%m-%s %H:%M:%S'), str((end - start).total_seconds())))

        start = datetime.datetime.now()
        if taskResponse == 7:
            filename = self.parametricDownloadFile(filename, taskID, stationList)
            end = datetime.datetime.now()
            print(
                """parametric download finish
            Start: %s
            End: %s
            Finish: %s""" % (
                    start.strftime('%Y-%m-%s %H:%M:%S'), end.strftime('%Y-%m-%s %H:%M:%S'),
                    str((end - start).total_seconds())))

        if counter > (maxTimeInMin * 60) / sleepSeconds:
            print('Process Took longer than {} minutes so was killed'.format(maxTimeInMin))

        return filename, taskResponse

    def request_task(self, payload):
        print(payload)

        stationList = []
        for i, item in enumerate(payload['parametricType']):
            stationList.append(item['stationType'])
        try:
            response = self.parametricSubmit(parameterDict=payload)
            jsonResponse = response.json()
            taskID, statusCode = jsonResponse['exportResponse']['taskId'], jsonResponse['statusCode']
            return taskID, statusCode
        except:
            return "None", "404"

    def check_task_states(self, filename, taskID, states_json_path, stationList, wait=True):
        """
        :param filename: - gz format, provide file name for data store
        :param taskID:
        :param states_json_path:
        :param stationList:
        :param wait:
        :return:
        """
        filename = self.parametricDownload(filename=filename, taskID=taskID, states_json_path=states_json_path,
                                           stationList=stationList, wait=wait)

# config_info = read_json_file(os.path.join(resources, "config.json"))
# server_config = read_json_file(os.path.join(resources, "service.json"))
# tokenID = read_json_file(os.path.join(resources, "token.json"))["tokenID"]
#
# t = Scrapy_Data(config_info, server_config, tokenID)
# t.parametricDownloadFile("/tmp/J80_FACT.gz", 71522.0)
