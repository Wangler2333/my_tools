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
            if dict_info.get("code", "11") == "1001" or dict_info.get("code", "11") == "1002":  # 如果返回的失败code 1001就显示红色
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

            special = config["download"]["special"]
            if special is False:
                request_info = payload_parameter(config)
            else:
                """API for special request set-up"""
                request_info = special_payload_parameter(config)

            taskID, statusCode = self.get_data.request_task(request_info)

            if int(statusCode) != 200:
                log_collect_append.logger.debug("Re-request %s" % str(i))
                taskID, statusCode = self.get_data.request_task(request_info)  # 增加一次 request retry

            tmp_dict = {"run info": i,
                        "product": product,
                        "station": station,
                        "code": str(int(statusCode)),  # """返回的code是float类型，需要先转成int再str"""
                        "Message": "request task",
                        "finished": False,
                        "taskID": taskID,
                        "retry": True}

            if int(statusCode) == 200:
                self.run_info[i] = tmp_dict
            else:
                tmp_dict["Message"] = "request fail"
                tmp_dict["code"] = "1002"
                tmp_dict["finished"] = True

            log_collect_append.logger.debug(tmp_dict)
            self.sinOut.emit(tmp_dict)

        running_list = list(self.run_info.items())

        timeOut = self.config_info.get("time out", 100)  # 设置超时
        times = 0

        get_states = False

        while self.working:

            """Check Task States"""

            for j in running_list:

                log_collect_append.logger.info(j)  # for debug review

                id = j[1]["taskID"]

                if id != "None":

                    get_states = False

                    for l in range(5):
                        try:
                            time.sleep(3)  # 加 delay 3s， 防止刷新频繁导致 request 报错
                            response = self.get_data.parametricStatus(id)  # 加异常retry，防止异常退出
                            if response:
                                get_states = True
                                break  # shit 漏掉了 break ...
                        except:
                            time.sleep(3)  # 如果出现异常就等待3秒
                            pass

                    log_collect_append.logger.debug("get_states: %s" % str(get_states))
                    if get_states is False:
                        break

                    jsonResponse = response.json()
                    log_collect_append.logger.info(jsonResponse)

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
                    log_collect_append.logger.debug(tmp)

                    if self.working is False:
                        break

                    if states_code == 6 and j[1]["retry"] is True:  # 如果 task Fail 进入
                        """重新提交 request 并删除原先的 taskID，记录新的 taskID, 允许三次Retry，Retry等待3秒"""
                        running_list.remove(j)

                        for i in range(3):
                            config = self.config_info["product-station-command"][j[1]["product"]][j[1]["station"]]
                            try:

                                special = config["download"]["special"]
                                if special is False:
                                    request_info = payload_parameter(config)
                                else:
                                    """API for special request set-up"""
                                    request_info = special_payload_parameter(config)

                                taskID, statusCode = self.get_data.request_task(request_info)
                                tmp_1 = {
                                    j[1]["run info"]:
                                        {
                                            "run info": j[1]["run info"],
                                            "product": j[1]["product"],
                                            "station": j[1]["station"],
                                            "code": str(int(statusCode)),
                                            "Message": "Re-request Task.",
                                            "finished": False,
                                            "taskID": taskID,
                                            "retry": False
                                        }
                                }
                                running_list.append(tmp_1)
                                log_collect_append.logger.info(tmp_1)
                            except:
                                time.sleep(3)
                                pass

                    if states_code == 6 and j[1]["retry"] is False:
                        running_list.remove(j)
                        continue

                    if states_code == 7:
                        """Download Data"""
                        local_file = os.path.join("/tmp",
                                                  ".".join([str(j[1]["product"]) + "_" + str(j[1]["station"]), "gz"]))

                        log_collect_append.logger.debug(local_file)  # 输出由于debug信息查看
                        log_collect_append.logger.debug(str(j[1]["station"]))
                        log_collect_append.logger.debug(id)

                        time.sleep(3)  # 新增下载等待，避免出现下载失败的情况.
                        for p in range(3):  # 增加 download retry，若出现 download 异常时等待三秒然后再次下载
                            try:
                                file_info = self.get_data.parametricDownloadFile(local_file, str(j[1]["station"]), id)

                                # 建议使用多进程下载数据，这样就不会影响UI界面更新等待

                                tmp["Message"] = "Download File [%s]" % file_info
                                self.sinOut.emit(tmp)
                                log_collect_append.logger.debug("Download File [%s]" % file_info)
                                running_list.remove(j)
                                log_collect_append.logger.debug("Remove: %s" % str(j))

                                if file_info:
                                    break
                            except:
                                time.sleep(3)
                                pass

                        """API for data process"""

                        if os.path.isfile(local_file):
                            t = DataProcess(local_file, tmp_path)
                            code, filePath = t.process()
                            log_collect_append.logger.info(code)
                            log_collect_append.logger.info(filePath)

                            if code == 0:
                                tmp["code"] = "1000"
                                tmp["Message"] = "Process Data Succeed!"
                                tmp["finished"] = True
                                self.sinOut.emit(tmp)

                                if result_dict.get(str(j[1]["product"]),
                                                   False) is False:  # try fix 多个任务时的结果重叠, use list replace dict
                                    result_dict[str(j[1]["product"])] = []

                                result_dict[str(j[1]["product"])].append(
                                    [str(j[1]["station"]), filePath])  # 改成内含list吧，字典格式在summary的时候处理起来比较麻烦

                            else:
                                tmp["code"] = "1001"
                                tmp["Message"] = "Process Data Failed!"
                                tmp["finished"] = True
                                self.sinOut.emit(tmp)
                            log_collect_append.logger.debug(result_dict)
                        else:
                            log_collect_append.logger.error("File not exist: %s" % local_file)

                else:
                    running_list.remove(j)
                    log_collect_append.logger.debug("Remove: %s" % str(j))

            if get_states is False:
                break

            if self.working is False:
                break

            times += 1
            log_collect_append.logger.info("Times: %s" % str(times))
            log_collect_append.logger.info(running_list)

            if len(running_list) == 0:
                break

            if times > timeOut:
                """当检查次数超出预设最大值时，进入此循环"""
                for io in running_list:
                    tmp_2 = {
                                "run info": io[1]["run info"],
                                "product": io[1]["product"],
                                "station": io[1]["station"],
                                "code": "101",
                                "Message": "Check Task State Time Out.",
                                "finished": True,
                    }
                    self.sinOut.emit(tmp_2)
                    log_collect_append.logger.error(tmp_2)
                break

        """API for all data to summary"""
        d = SummaryData(result_dict)
        state = d.run()
        self.sinOut.emit({"FINISHED ALL": state})
