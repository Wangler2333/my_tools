#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time   : 3/14/18 10:48 PM
# @Author : Saseny.Zhou
# @File   : main.py

from PyQt5.QtWidgets import *
from UI.ui_main import *
from AppThread.threadForUI import *


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

        self.setCombox()

    def setCombox(self):
        try:
            functions = self.configInfo["function"].keys()
            self.comboBox.addItems(functions)
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
        self.errorInfo = read_json_file(errorJsonPath)
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

        """功能线程"""
        self.runThread = WorkRunning(self.configInfo, item, self.unitsInfo, self.errorInfo)
        self.runThread.start()
        self.runThread.runSignal.connect(self.checkState)

    def checkState(self, dict):
        if dict["action"] == "Observation":
            self.observation_check(dict)
        if dict["action"] == "Yield Report":
            self.yield_report(dict)

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

    def yield_report(self, info):
        print(info)
        if info.get("finished",False) is not False:
            self.label_2.setText(info["message"])

        if info.get("finished",False) is True:
            self.label_2.setText("处理结束!")
            self.label_2.setStyleSheet("background-color: rgb(0, 255, 0);")
            self.runTime.stop()
            self.setButtonFunction(True)

    def searchInfo(self):
        pass

    def lcdShow(self, number):
        self.lcdNumber.display(number)

    def labelChange(self, string):
        self.label_2.setText(string)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainTools()
    mainWindow.show()
    sys.exit(app.exec())
