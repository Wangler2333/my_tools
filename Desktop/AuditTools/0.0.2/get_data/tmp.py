#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time     : 2018/2/26下午1:54
# @Author   : Saseny Zhou
# @Site     : 
# @File     : tmp.py
# @Software : PyCharm


import requests
import datetime
from config.plot import *
import threading
import queue

q = queue.Queue(0)
myLock = threading.Lock()
NUM_WORKERS = 5


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

        if type(payload) != str:
            payload = json.dumps(payload)
        response = requests.post(fullUrl, data=payload, headers=headers)
        print(fullUrl)

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

    def parametricDownloadFile(self, local_filename, taskID, stationType):
        API_TYPE = "PARAMETRIC-DOWNLOAD"
        fullUrl = self.url + self.serviceDict["PFA"][API_TYPE]["service"]
        fullUrl = fullUrl.replace("<TASKID>", str(int(taskID))).replace("<STATIONTYPE>", stationType)
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'mop_session_id': self.tokenID}
        r = requests.get(fullUrl, headers=headers, stream=True)
        # local_filename='test.gz'

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

    def request_task(self, project, overlay, startDate, endDate, station, ):
        """One by one station"""
        payload = payload_parameter(station, startDate, endDate, project, overlay)
        stationList = []
        for i, item in enumerate(payload['parametricType']):
            stationList.append(item['stationType'])

        response = self.parametricSubmit(parameterDict=payload)
        jsonResponse = response.json()
        taskID, statusCode = jsonResponse['exportResponse']['taskId'], jsonResponse['statusCode']

        return taskID, statusCode

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


class Scrapy_Thread(threading.Thread):
    def __init__(self, input, work):
        self.working = True
        self._job_q = input
        self._work_type = work
        threading.Thread.__init__(self)

    def __del__(self):
        self.working = False

    def run(self):
        while self.working:
            if self._job_q.qsize() > 0:
                self._process_job(self._job_q.get(), self._work_type)
            else:
                break

    def _process_job(self, job, work):
        doJob(job, work)


def doJob(job, work):
    myLock.acquire()
    time.sleep(1)
    print(job, work)
    myLock.release()


def thread_main(run_list):
    for i in run_list:
        q.put(i)
    print("Total %s" % str(q.qsize()))
    for x in range(NUM_WORKERS):
        Scrapy_Thread(q, x).start()
