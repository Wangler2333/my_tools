#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time   : 3/14/18 10:48 PM
# @Author : Saseny.Zhou
# @File   : main.py

from UI.ui_main import *
from AppThread.threadForUI import *
from MacOS.show import *
from MacOS.search import *


class MainTools(QMainWindow, Ui_BurninTools):
    def __init__(self):
        super(MainTools, self).__init__()
        self.setupUi(self)
        self.configInfo = read_json_file(configJsonPath)

        self.unitsInfo = read_json_file(unitJsonPath)
        if self.unitsInfo is False:
            self.unitsInfo = {}

        self.errorInfo = read_json_file(errorJsonPath)
        if self.errorInfo is False:
            self.errorInfo = {}

        self.historyInfo = read_json_file(historyJsonPath)
        if self.historyInfo is False:
            self.historyInfo = {}

        self.errorMessage = read_json_file(errorMessageJsonPath)
        if self.errorMessage is False:
            self.errorMessage = {}

        self.additional = {}

        self.setComboBox()

    def setComboBox(self):
        try:
            functions = self.configInfo["function"].keys()
            self.comboBox.addItems(functions)
            if self.historyInfo.get("function", False) is not False:
                self.comboBox.setCurrentText(str(self.historyInfo["function"]))
        except:
            collectionData.logger.error("No Config read!")
            pass

    def setButtonFunction(self, flag=False):
        if flag is False:
            self.pushButton.setEnabled(False)
            self.actionload_units.setEnabled(False)
            self.actionload_error.setEnabled(False)
        else:
            self.pushButton.setEnabled(True)
            self.actionload_units.setEnabled(True)
            self.actionload_error.setEnabled(True)

    def loadUnits(self):
        unit_number_file_to_json(self.configInfo)
        self.unitsInfo = read_json_file(unitJsonPath)
        self.label_2.setText("机器信息加载成功!")

    def loadError(self):
        error_code_file_to_json(self.configInfo)
        read_error_message_to_json(os.path.join(resources, self.configInfo["process"]["Excel Read"]["file name"]))
        self.errorInfo = read_json_file(errorJsonPath)
        self.errorMessage = read_json_file(errorMessageJsonPath)
        self.label_2.setText("Error信息加载成功!")

    def start(self):
        collectionData.logger.info("Click Start Button.")
        self.label_2.setStyleSheet("background-color: rgb(255, 255, 0);")
        self.label_2.setText("正在处理...")
        self.setButtonFunction(False)

        """时间线程"""
        self.runTime = TimeCalculate()
        self.runTime.start()
        self.runTime.timeSignal.connect(self.lcdShow)

        """选项"""
        item = self.comboBox.currentText()
        self.record(item)

        """Observation报表时需要添加其他信息"""
        if item == "Observation Report":
            self.observation_report()

        """功能线程"""
        self.runThread = WorkRunning(configInfo=self.configInfo, action=item, unitsInfo=self.unitsInfo,
                                     errorInfo=self.errorInfo, errorMessage=self.errorMessage,
                                     additional=self.additional)
        self.runThread.start()
        self.runThread.runSignal.connect(self.checkState)

    def record(self, item):
        currentTime = time.strftime("%Y-%m-%d %H:%M:%S")
        dict_info = {
            "function": item,
            "time": currentTime
        }
        write_json_file(dict_info, historyJsonPath)

    def checkState(self, dict):
        if dict["action"] == "Observation":
            self.observation_check(dict)
        if dict["action"] == "Yield Report":
            self.yield_report(dict)
        if dict["action"] == "Log Collection":
            self.log_collection(dict)

    def log_collection(self, info):
        self.label_2.setText(info["message"])
        if info.get("finished", False) is True:
            self.label_2.setText("处理结束!")
            self.label_2.setStyleSheet("background-color: rgb(0, 255, 0);")
            self.runTime.stop()
            self.setButtonFunction(True)

    def observation_check(self, info):
        print(info)
        result = info["result"]
        finish = info["finished"]
        if result["special"] is True:
            while True:
                text, ok = QInputDialog.getText(self, '输入信息', '输入格子编号:')
                if ok:
                    if re.findall(r'[A-z]\d{5}-\d{2}', str(text)):
                        id = str(text).upper()
                        break
        else:
            id = "None"
        write_observation(serial_number=result["serial number"], dti_info=result["dti info"],
                          path_road=result["path road"], rack_id=str(id))
        self.label_2.setText("处理结束!")
        self.label_2.setStyleSheet("background-color: rgb(0, 255, 0);")
        self.runTime.stop()
        self.setButtonFunction(True)

    def observation_report(self):
        self.additional = {}

    def yield_report(self, info):
        self.label_2.setText(info["message"])

        if info.get("show error", False) is True:
            self.show_error_info = ShowError(info["info"])
            self.show_error_info.show()
            self.show_error_info.move(200,200)

        if info.get("finished", False) is True:
            self.label_2.setText("处理结束!")
            self.label_2.setStyleSheet("background-color: rgb(0, 255, 0);")
            self.runTime.stop()
            self.setButtonFunction(True)

    def searchInfo(self):
        self.search = SearchInfo(self.errorMessage, self.unitsInfo)
        self.search.show()

    def lcdShow(self, number):
        self.lcdNumber.display(number)

    def labelChange(self, string):
        self.label_2.setText(string)

    def closeEvent(self, QCloseEvent):
        try:
            self.show_error_info.close()
        except:
            pass
        try:
            self.search.close()
        except:
            pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainTools()
    mainWindow.show()
    sys.exit(app.exec())
