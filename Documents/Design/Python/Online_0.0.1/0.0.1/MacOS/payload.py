#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time     : 2018/3/7下午6:21
# @Author   : Saseny Zhou
# @Site     : 
# @File     : payload.py
# @Software : PyCharm


from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from UI.ui_payload import *
from Path.path import *


class PayLoad(QMainWindow, Ui_payload):
    """
    QApplication.processEvents()
    """
    confirmSignal = pyqtSignal(dict)

    def __init__(self, loginStates, product, station):
        super(PayLoad, self).__init__()

        self.setupUi(self)
        self.center()

        self.setWindowFlags(QtCore.Qt.CustomizeWindowHint | QtCore.Qt.FramelessWindowHint)
        # 隐藏窗口工具栏   | QtCore.Qt.FramelessWindowHint

        self.loginStates = loginStates
        self.product = product
        self.station = station
        self.mainConfig = read_json_file(os.path.join(resources, "config.json"))
        self.configInfo = self.mainConfig["product-station-command"]
        self.parametricTypeList = []

        self.stationType.setText(self.station)
        self.productCode.setText(self.product)

        self.setFixedSize(self.width(), self.height())

        self.setReadOnly()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def setReadOnly(self):
        stationConfig = self.configInfo[self.product][self.station]
        self.stationType.setStyleSheet('font: 10pt ".SF NS Text";')
        self.overlayVersion.setStyleSheet('font: 8pt ".SF NS Text";')
        self.overlayVersion.setText(",".join(stationConfig["download"]["overlay"]))
        self.commandShow.setStyleSheet('font: 8pt ".SF NS Text";')
        self.commandShow.setText(resources + stationConfig["cmd-link"])
        self.lineEdit.setStyleSheet('font: 8pt ".SF NS Text";')
        self.lineEdit.setText(resources + stationConfig["config"])
        if self.loginStates is False:
            for i in [self.siteName, self.auditOnly, self.limitsVersion, self.selectAll, self.dataCategory,
                      self.requestColumns, self.textCategory, self.passFailCategory, self.nullIncluded,
                      self.samplePercent, self.frequency]:
                i.setStyleSheet("background-color: rgb(218, 255, 250);")
                i.setReadOnly(True)

    def addStationButton(self):
        childParametric = {
            "stationType": self.stationType.text(),
            "overlayVersion": [],
            "limitsVersion": [],
            "selectAll": ""
        }
        if self.selectAll.text():
            if self.selectAll.text() == "false":
                childParametric["selectAll"] = False
            else:
                childParametric["selectAll"] = True

        if self.overlayVersion.text():
            if "," in self.overlayVersion.text():
                childParametric["overlayVersion"].extend(str(self.overlayVersion.text()).split(","))
            else:
                childParametric["overlayVersion"].append(self.overlayVersion.text())

        if self.limitsVersion.text():
            if "," in self.limitsVersion.text():
                childParametric["limitsVersion"].extend(str(self.limitsVersion.text()).split(","))
            else:
                childParametric["limitsVersion"].append(self.limitsVersion.text())

        self.parametricTypeList.append(childParametric)
        self.stationCount.display(len(self.parametricTypeList))

    def openFileButton(self):
        serialNumberFile, _ = QFileDialog.getOpenFileName(self, "Load New Config", "/", "file (*.txt)")
        if serialNumberFile:
            with open(serialNumberFile, "r") as f:
                reader = f.read()
            rule = self.mainConfig["serial number read"]["rule"]
            snList = re.findall(rule, str(reader))
            if len(snList) > 0:
                snList = [x for x in set(snList)]
                self.serialNumber.setText(",".join(snList))

    def cmdReplaceButton(self):
        commandFile, _ = QFileDialog.getOpenFileName(self, "Load New Config", "/", "file (*.py)")
        if commandFile:
            self.commandShow.setText(commandFile)

    def cfgReplaceButton(self):
        configFile, _ = QFileDialog.getOpenFileName(self, "Load New Config", "/", "file (*.json)")
        if configFile:
            self.lineEdit.setText(configFile)

    def cancelButton(self):
        self.close()

    def getInfo(self):
        self.addStationButton()
        new = []
        """Station Type 去重"""
        for i in self.parametricTypeList:
            if i not in new:
                new.append(i)

        serialNumber = "N"
        if self.serialNumber.toPlainText():
            serialNumber = []
            if "," in self.serialNumber.toPlainText():
                serialNumber.extend(str(self.serialNumber.toPlainText()).split(","))
            else:
                serialNumber.append(self.serialNumber.toPlainText())

        dictInfo = {
            "siteName": [self.siteName.text()],
            "auditOnly": self.auditOnly.text(),
            "parametricType": new,
            "dataCategory": [self.dataCategory.text()],
            "requestedColumns": str(self.requestColumns.toPlainText()).split(","),
            "testCategory": [self.textCategory.text()],
            "modules": self.modules.text(),
            "passFailCategory": [self.passFailCategory.text()],
            "attributes": self.attributes.text(),
            "nullIncluded": self.nullIncluded.text(),
            "samplePercent": self.samplePercent.text(),
            "startTime": self.startTime.text(),
            "endTime": self.endTime.text(),
            "frequency": self.frequency.text(),
            "productCode": [self.productCode.text()],
            "serialNumber": serialNumber,
            "command": self.commandShow.text(),
            "config": self.lineEdit.text(),
            "explain": self.configInfo[self.productCode.text()][new[0]["stationType"]]["explain"]
        }
        return dictInfo

    def confirmButton(self):
        self.confirmSignal.emit(self.getInfo())
