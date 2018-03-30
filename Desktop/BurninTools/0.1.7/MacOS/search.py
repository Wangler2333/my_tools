#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time     : 2018/3/16下午12:23
# @Author   : Saseny Zhou
# @Site     : 
# @File     : search.py
# @Software : PyCharm


from PyQt5.QtWidgets import *
from UI.ui_search import *


class SearchInfo(QMainWindow, Ui_search):
    def __init__(self, errorMessage, unitsInfo):
        super(SearchInfo, self).__init__()
        self.setupUi(self)
        self.comboBox.addItems(["Serial Number", "Unit Number"])
        self.errorMessage = errorMessage
        self.unitsInfo = unitsInfo

    def search(self):
        self.columnView.clear()
        choose = self.comboBox.currentText()
        item = self.lineEdit.text()
        if choose == "Serial Number":
            self.checkFromSerialNumber(item)
        if choose == "Unit Number":
            self.checkFromUnitNumber(item)

    def checkFromSerialNumber(self, sn):
        unit = self.unitsInfo.get(sn, False)
        error = self.errorMessage.get(sn, False)
        if unit is False:
            unit = {
                "wip": "找到该机器信息.",
                "number": "未找到该机器信息.",
                "config": "未找到该机器信息."
            }
        if error is False:
            error = []
        self.showInfo(unit, error)

    def checkFromUnitNumber(self, unit):
        serial_number = "None"
        for i in self.unitsInfo.items():
            if str(unit) == i[1]["number"]:
                serial_number = str(i[0])
                break
        self.checkFromSerialNumber(serial_number)

    def showInfo(self, unit, error):
        self.lineEdit_2.setText(unit["wip"])
        self.lineEdit_3.setText(unit["number"])
        self.lineEdit_4.setText(unit["config"])
        self.columnView.addItems(error)
