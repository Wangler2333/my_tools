#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time     : 2018/3/8下午3:04
# @Author   : Saseny Zhou
# @Site     : 
# @File     : running.py
# @Software : PyCharm

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from UI.ui_running import *
from API.download import *
from Functions.shell import *


class Running(QMainWindow, Ui_running):
    quitSignal = pyqtSignal(bool)

    def __init__(self, dictInfo):
        super(Running, self).__init__()
        self.setupUi(self)
        self.center()
        self.dictInfo = dictInfo
        self.logAppend.setStyleSheet('background-color: rgb(245, 255, 254);'
                                     'font: 25 12pt "STFangsong";')
        self.input_list = []
        self.sendThreadList = []
        self.show_list()
        self.startRunning()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def show_list(self):
        for i in self.dictInfo:
            product = str(i["productCode"][0])
            station = str(i["parametricType"][0]["stationType"])
            nameInfo = interval.join([product, station])
            if nameInfo not in self.input_list:
                self.sendThreadList.append({nameInfo: i})
                self.input_list.append(nameInfo)
        count = 0
        for i in self.input_list:
            new_item = QTableWidgetItem(str(i).replace(interval, " "))
            item_info = QTableWidgetItem("Pending")
            new_item.setTextAlignment(QtCore.Qt.AlignCenter)
            new_item.setBackground(QColor(255, 255, 0))
            item_info.setTextAlignment(QtCore.Qt.AlignCenter)
            self.statesCheck.setItem(count, 0, new_item)
            self.statesCheck.setItem(count, 1, item_info)
            count += 1

    def logShowAppend(self, message):
        QApplication.processEvents()
        if "ERROR" in message or "WARNING" in message:
            self.logAppend.append("<font color=%s>%s</font>" % ("red", message))
        elif "INFO" in message or "DEBUG" in message:
            self.logAppend.append("<font color=%s>%s</font>" % ("black", message))
        else:
            self.logAppend.append("<font color=%s>%s</font>" % ("blue", message))

    def logCheckButton(self):
        os.system("open {}".format(os.path.join(resources, "Logs", "debug.log")))

    def startRunning(self):
        self.running = WorkThread(self.sendThreadList)
        self.running.start()
        self.running.threadSignal.connect(self.showStates)

    def showStates(self, dictInfo):
        if dictInfo.get("message", False) is not False:
            self.logShowAppend(dictInfo["message"])
        if dictInfo.get("run info", None) is not None or dictInfo.get("code", None) is not None:
            self.flash_states(dictInfo)

    def flash_states(self, dict_info):
        code_info = read_json_file(os.path.join(resources, "code.json"))
        row = self.input_list.index(dict_info["run info"])
        name = code_info.get(str(dict_info["code"]), "UNDOCUMENTED RETURN [Code %s]" % str(dict_info["code"]))
        new_item = QTableWidgetItem(str(name))
        new_item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.statesCheck.setItem(int(row), 1, new_item)

        if dict_info["finished"] is True:
            new_color = QTableWidgetItem(str(dict_info["run info"]).replace(interval, " "))
            new_color.setTextAlignment(QtCore.Qt.AlignCenter)
            new_color.setBackground(QColor(0, 255, 0))
            if dict_info.get("code", "10000") in ["1001", "1002", "400"]:
                new_color.setBackground(QColor(255, 0, 0))
            self.statesCheck.setItem(int(row), 0, new_color)

    def closeEvent(self, QCloseEvent):
        self.running.stop()
        collectLogs.logger.info("Running Window Close")
        self.quitSignal.emit(True)


class WorkThread(QThread):
    threadSignal = pyqtSignal(dict)

    def __init__(self, dictInfo):
        super(WorkThread, self).__init__()
        self.working = True
        self.dictInfo = dictInfo
        self.tokenCode = read_json_file(os.path.join(resources, "token.json"))
        self.url = read_json_file(os.path.join(resources, "config.json"))
        self.server = read_json_file(os.path.join(resources, "service.json"))

    def stop(self):
        self.working = False

    def messageSet(self, key, string):
        if key == "ERROR":
            collectLogs.logger.error(str(string))
            return "[ERROR][{}] {}".format(time.strftime("%Y-%m-%d %H:%M:%S"), str(string))
        elif key == "DEBUG":
            collectLogs.logger.debug(str(string))
            return "[DEBUG][{}] {}".format(time.strftime("%Y-%m-%d %H:%M:%S"), str(string))
        elif key == "INFO":
            collectLogs.logger.info(str(string))
            return "[INFO][{}] {}".format(time.strftime("%Y-%m-%d %H:%M:%S"), str(string))
        elif key == "WARNING":
            collectLogs.logger.warning(str(string))
            return "[WARNING][{}] {}".format(time.strftime("%Y-%m-%d %H:%M:%S"), str(string))
        else:
            collectLogs.logger.info(str(string))
            return "[{}]\n {}".format(time.strftime("%Y-%m-%d %H:%M:%S"), str(string))

    def dictReturnInfo(self, Station=None, Code=None, String=None, taskID=None, Key=None, Finished=False):
        try:
            tmp = str(Station).split(interval)
            product = tmp[0]
            station = tmp[1]
        except:
            product = False
            station = False
        info = {
            "run info": Station,
            "product": product,
            "station": station,
            "code": Code,
            "taskID": taskID,
            "message": self.messageSet(Key, String),
            "finished": Finished
        }
        return info

    def run(self):
        time_out = self.url["time out"]
        count = 1

        self.threadSignal.emit(self.dictReturnInfo(String=self.dictInfo))
        self.threadSignal.emit(self.dictReturnInfo(String="Time Out SetUp: {}".format(time_out)))
        if self.tokenCode is not False:
            codeId = self.tokenCode["tokenID"]

            download_class = Scrapy_Data(self.url["url"], self.server, codeId)

            self.threadSignal.emit(self.dictReturnInfo(String=self.tokenCode))
            self.threadSignal.emit(self.dictReturnInfo(String=self.url["url"]))
            collectLogs.logger.debug(self.tokenCode)
            collectLogs.logger.debug(self.url["url"])
            collectLogs.logger.debug(self.server)

            request_succeed = []

            time.sleep(0.5)
            for i in self.dictInfo:
                for j in i.keys():
                    run_info = j
                    payload_info = i[j]
                    self.threadSignal.emit(self.dictReturnInfo(Station=run_info, Key="INFO",
                                                               String="Start {} get data request".format(run_info)))
                    collectLogs.logger.info("Start {} get data request".format(run_info))

                    if self.working is False:
                        break

                    """Request Get Data"""
                    for n in range(2):

                        taskID, statusCode = download_class.request_task(payload_info)

                        if self.working is False:
                            break

                        if statusCode == 200:
                            self.threadSignal.emit(
                                self.dictReturnInfo(Station=run_info, Key="INFO", Code=str(statusCode),
                                                    taskID=taskID,
                                                    String="{} request return info: taskID - {}, code - {}".format(
                                                        run_info, taskID, statusCode)))
                            collectLogs.logger.info(
                                "{} request return info: taskID - {}, code - {}".format(run_info, taskID,
                                                                                        statusCode))

                            request_succeed.append([run_info, taskID])
                            break

                        self.threadSignal.emit(
                            self.dictReturnInfo(Station=run_info, Key="ERROR", Code="400", taskID=taskID,
                                                String="{} request return info: taskID - {}, code - {}".format(
                                                    run_info, taskID, "400")))
                        collectLogs.logger.error(
                            "{} request return info: taskID - {}, code - {}".format(run_info, taskID, "400"))

                        self.threadSignal.emit(self.dictReturnInfo(Key="INFO", String="Re-request delay time 3s"))
                        collectLogs.logger.info("sleep 3")
                        time.sleep(3)

                    if len(request_succeed) == 0:
                        self.threadSignal.emit(
                            self.dictReturnInfo(Station=run_info, Key="ERROR", Code="400", Finished=True,
                                                String="{} request return info: taskID - {}, code - {}".format(
                                                    run_info, "None", "400")))
                    else:
                        for i in request_succeed:
                            if run_info not in i:
                                self.threadSignal.emit(
                                    self.dictReturnInfo(Station=run_info, Key="ERROR", Code="400", Finished=True,
                                                        String="{} request return info: taskID - {}, code - {}".format(
                                                            run_info, "None", "400")))

            if self.working is not False and len(request_succeed) != 0:
                while self.working:
                    count += 1
                    if count >= time_out:
                        for g in request_succeed:
                            self.threadSignal.emit(self.dictReturnInfo(Station=g[0], Code="1002"))
                        self.threadSignal.emit(self.dictReturnInfo(Key="ERROR", String="Time Out: {}".format(count)))
                        collectLogs.logger.error("Time Out: {}".format(count))
                        break

                    for i in request_succeed:
                        self.threadSignal.emit(self.dictReturnInfo(Station=i[0], Key="INFO",
                                                                   String="Get taskID:{} current status.".format(i[1])))
                        get_states = False
                        for n in range(3):
                            response = download_class.parametricStatus(str(int(i[1])))
                            if response:
                                get_states = True
                                break

                        self.threadSignal.emit(
                            self.dictReturnInfo(Key="INFO", String="Get Status: {}".format(get_states)))
                        collectLogs.logger.info("Get Status: {}".format(get_states))

                        if get_states is False:
                            continue

                        try:
                            jsonResponse = response.json()
                            states_code = jsonResponse['exportResponse']['taskStatus']
                            self.threadSignal.emit(self.dictReturnInfo(Station=i[0], Key="INFO", Code=states_code,
                                                                       String="Current Get status: {}".format(
                                                                           jsonResponse),
                                                                       taskID=i[1]))
                            collectLogs.logger.info(String="Current Get status: {}".format(jsonResponse))
                        except:
                            states_code = 404
                            self.threadSignal.emit(self.dictReturnInfo(Station=i[0], Key="ERROR", Code=states_code,
                                                                       String="Current Get status: {}".format(
                                                                           states_code),
                                                                       taskID=i[1]))
                            collectLogs.logger.error(String="Current Get status: {}".format(states_code))
                            request_succeed.remove(i)
                            self.threadSignal.emit(
                                self.dictReturnInfo(Key="DEBUG", String="Remove Download Item: {}".format(i)))
                            collectLogs.logger.debug("Remove Download Item: {}".format(i))

                        if self.working is False:
                            break

                        if states_code == 7:
                            """Download Data"""
                            local_file = os.path.join("/tmp", ".".join(
                                [str(i[0]).split(interval)[0] + "_" + str(i[0]).split(interval)[1], "gz"]))
                            self.threadSignal.emit(
                                self.dictReturnInfo(Key="INFO",
                                                    String="Start Download Item: {}, TMP File Path: {}".format(i,
                                                                                                               local_file)))
                            collectLogs.logger.info("Start Download Item: {}, TMP File Path: {}".format(i, local_file))

                            time.sleep(3)  # 新增下载等待，避免出现下载失败的情况.
                            self.threadSignal.emit(self.dictReturnInfo(Key="INFO", String="Delay time 3s"))
                            collectLogs.logger.info("sleep 3")

                            for p in range(3):  # 增加 download retry，若出现 download 异常时等待三秒然后再次下载
                                try:
                                    file_info = self.get_data.parametricDownloadFile(local_file,
                                                                                     str(i[0]).split(interval)[1],
                                                                                     str(int(i[1])))
                                    if file_info:
                                        self.threadSignal.emit(
                                            self.dictReturnInfo(Key="INFO", Station=i[0], Code=states_code, taskID=i[1],
                                                                String="Download Data Finished: {}".format(i[0])))
                                        collectLogs.logger.info("Download Data Finished: {}".format(i[0]))
                                        break
                                except:
                                    time.sleep(3)
                                    pass

                            if self.working is False:
                                break

                            if os.path.isfile(local_file):
                                path = os.path.join(os.path.expanduser("~"), "Downloads", "OnLineData")

                                if not os.path.isdir(path):
                                    os.makedirs(path)

                                currentPath = os.path.join(path, time.strftime("%Y_%m_%d-%H"))
                                if not os.path.isdir(currentPath):
                                    os.makedirs(currentPath)

                                shutil.copy(local_file, currentPath)
                                self.threadSignal.emit(
                                    self.dictReturnInfo(Key="INFO", String="Copy File: From {} to {}".format(local_file,
                                                                                                             currentPath)))
                                collectLogs.logger.info("Copy File: From {} to {}".format(local_file, currentPath))

                                time.sleep(0.5)

                                self.threadSignal.emit(
                                    self.dictReturnInfo(Key="INFO", Station=i[0], Code=states_code, taskID=i[1],
                                                        String="Start Processing Data: {}".format(i[0])))
                                collectLogs.logger.info("Start Processing Data: {}".format(i[0]))

                                if self.working is False:
                                    break

                                for p in self.dictInfo:
                                    if p.get(i[0], True) is True:
                                        tmp = p[i[0]]
                                        cmd = " ".join([tmp["explain"], tmp["command"], os.path.join(currentPath,
                                                                                                     os.path.basename(
                                                                                                         local_file))])

                                        self.threadSignal.emit(
                                            self.dictReturnInfo(Key="INFO", String="Run Command: {}".format(cmd)))
                                        collectLogs.logger.info("Run Command: {}".format(cmd))

                                        time.sleep(1)

                                        finish = shell(cmd)

                                        if finish == 0:
                                            self.threadSignal.emit(
                                                self.dictReturnInfo(Key="INFO",
                                                                    String="Process Finished: {}".format(i[0]),
                                                                    Finished=True, Code="1000", taskID=i[1]))
                                            collectLogs.logger.info("Process Finished: {}".format(i[0]))
                                            request_succeed.remove(i)

                                        else:
                                            self.threadSignal.emit(
                                                self.dictReturnInfo(Key="ERROR",
                                                                    String="Process Failed: {}".format(i[0]),
                                                                    Finished=True, Code="1001", taskID=i[1]))
                                            collectLogs.logger.error("Process Failed: {}".format(i[0]))
                                            request_succeed.remove(i)

                    if self.working is False:
                        break
