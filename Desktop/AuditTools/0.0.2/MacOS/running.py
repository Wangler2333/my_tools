#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time     : 2018/2/8下午1:17
# @Author   : Saseny Zhou
# @Site     : 
# @File     : running.py
# @Software : PyCharm


from UI.ui_running import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from get_data.scrap_data import *
from config.plot import *
from functions.process_data import *
from functions.summary_data import *


class RunningShow(QMainWindow, Ui_Running):
    close_signal = pyqtSignal()

    def __init__(self, run_list):
        super(RunningShow, self).__init__()
        self.setupUi(self)
        self.input_list = run_list
        self.show_list()
        self.start_running()

    def show_list(self):
        count = 0
        for i in self.input_list:
            new_item = QTableWidgetItem(str(i).replace(interval, " "))
            item_info = QTableWidgetItem("Pending")
            new_item.setTextAlignment(QtCore.Qt.AlignCenter)
            new_item.setBackground(QColor(255, 255, 0))
            item_info.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(count, 0, new_item)
            self.tableWidget.setItem(count, 1, item_info)
            count += 1

    def start_running(self):
        self.threadWorkd = WorkerList(self.input_list)
        self.threadWorkd.start()
        self.threadWorkd.sinOut.connect(self.return_check)

    def return_check(self, dict_info):
        if dict_info.get("FINISHED ALL", False) is False:
            self.append_logs(" [" + dict_info["run info"] + "] " + dict_info["Message"])
            self.flash_states(dict_info)
        else:
            self.append_logs("All Process Finished!")

    def append_logs(self, message):
        QApplication.processEvents()
        current = time.strftime("%Y-%m-%d %H:%M:%S")
        self.textEdit.append(str(current) + " -- " + str(message))

    def flash_states(self, dict_info):
        code_info = read_json_file(os.path.join(resources, "code.json"))
        row = self.input_list.index(dict_info["run info"])
        name = code_info.get(str(dict_info["code"]), "UNDOCUMENTED RETURN [Code %s]" % str(dict_info["code"]))
        new_item = QTableWidgetItem(str(name))
        new_item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(int(row), 1, new_item)

        if dict_info.get("finished", False) is True:
            new_color = QTableWidgetItem(str(dict_info["run info"]).replace(interval, " "))
            new_color.setTextAlignment(QtCore.Qt.AlignCenter)
            new_color.setBackground(QColor(0, 255, 0))
            if dict_info.get("code", "11") != "0":
                new_color.setBackground(QColor(255, 0, 0))
            self.tableWidget.setItem(int(row), 0, new_color)

    def closeEvent(self, event):
        self.close_signal.emit()
        self.close()
        self.threadWorkd.__del__()


class WorkerList(QThread):
    sinOut = pyqtSignal(dict)

    def __init__(self, list_info, parent=None):
        super(WorkerList, self).__init__(parent)
        self.working = True
        self.run_info = list_info
        self.list_dict()
        self.run_info = {}
        self.config_info = read_json_file(os.path.join(resources, "config.json"))
        self.server_config = read_json_file(os.path.join(resources, "service.json"))
        try:
            self.tokenID = read_json_file(os.path.join(resources, "token.json"))["tokenID"]
        except:
            self.tokenID = "None"
        self.get_data = Scrapy_Data(self.config_info, self.server_config, self.tokenID)

    def __del__(self):
        self.working = False
        self.wait()

    def list_dict(self):
        self.dict_info = {}
        for i in self.run_info:
            self.dict_info[i] = {}

    def run(self):
        result_dict = {}
        os.system("rm -rf /tmp/*.gz")

        for i in self.dict_info.keys():

            if self.working is False:
                break

            """Request Task"""

            product = str(i).split(interval)[0]
            station = str(i).split(interval)[1]
            config = self.config_info["product-station-command"][product][station]
            request_info = payload_parameter(config)
            taskID, statusCode = self.get_data.request_task(request_info)

            if int(statusCode) != 200:
                taskID, statusCode = self.get_data.request_task(request_info)  # 增加一次 request retry

            tmp_dict = {"run info": i,
                        "product": product,
                        "station": station,
                        "code": str(int(statusCode)),  # """返回的code是float类型，需要先转成int再str"""
                        "Message": "request task",
                        "finished": False,
                        "taskID": taskID}
            if int(statusCode) == 200:
                self.run_info[i] = tmp_dict
            else:
                tmp_dict["Message"] = "request fail"

            print(tmp_dict)

            self.sinOut.emit(tmp_dict)

        running_list = list(self.run_info.items())

        timeOut = self.config_info.get("time out", 100)  # 设置超时
        times = 0

        get_states = False

        while self.working:

            """Check Task States"""

            for j in running_list:

                id = j[1]["taskID"]

                if id != "None":

                    get_states = False

                    for l in range(5):
                        try:
                            time.sleep(3)     # 加 delay 3s， 防止刷新频繁导致 request 报错
                            response = self.get_data.parametricStatus(id)  # 加异常retry，防止异常退出
                            if response:
                                get_states = True
                                break      # shit 漏掉了 break ...
                        except:
                            time.sleep(3)  # 如果出现异常就等待3秒
                            pass

                    if get_states is False:
                        break

                    jsonResponse = response.json()

                    try:
                        states_code = jsonResponse['exportResponse']['taskStatus']
                    except:
                        states_code = 404
                    tmp = {"run info": j[1]["run info"],
                           "product": j[1]["product"],
                           "station": j[1]["station"],
                           "code": str(int(states_code)),  # """返回的code是float类型，需要先转成int再str"""
                           "Message": "Check task states.",
                           "finished": False,
                           "taskID": id}
                    self.sinOut.emit(tmp)

                    if self.working is False:
                        break

                    if states_code == 7:
                        """Download Data"""
                        local_file = os.path.join("/tmp",
                                                  ".".join([str(j[1]["product"]) + "_" + str(j[1]["station"]), "gz"]))

                        print(local_file)  # 输出由于debug信息查看
                        print(str(j[1]["station"]))
                        print(id)

                        file_info = self.get_data.parametricDownloadFile(local_file, str(j[1]["station"]),
                                                                         id)  # 建议使用多进程下载数据，这样就不会影响UI界面更新等待

                        tmp["Message"] = "Download File [%s]" % file_info
                        self.sinOut.emit(tmp)
                        print("Download File [%s]" % file_info)
                        running_list.remove(j)

                        """API for data process"""
                        t = DataProcess(local_file, tmp_path)
                        code, filePath = t.process()
                        print(code, filePath)
                        if code == 0:
                            tmp["code"] = "1000"
                            tmp["Message"] = "Process Data Succeed!"
                            tmp["finished"] = True
                            self.sinOut.emit(tmp)
                            result_dict[str(j[1]["product"])] = {
                                str(j[1]["station"]): filePath}
                        else:
                            tmp["code"] = "1001"
                            tmp["Message"] = "Process Data Failed!"
                            tmp["finished"] = True
                            self.sinOut.emit(tmp)
                        print(result_dict)

                else:
                    running_list.remove(j)

            if get_states is False:
                break

            if self.working is False:
                break

            times += 1
            print("Times: %s" % str(times))

            if len(running_list) == 0:
                break
            if times > timeOut:
                break

        """API for all data to summary"""
        d = SummaryData(result_dict)
        state = d.run()
        self.sinOut.emit({"FINISHED ALL": state})
