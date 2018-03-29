#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time     : 2018/3/7下午5:13
# @Author   : Saseny Zhou
# @Site     : 
# @File     : ui_payload.py
# @Software : PyCharm

from PyQt5 import QtCore, QtGui, QtWidgets
from Path.path import *


class Ui_payload(object):
    def setupUi(self, payload):
        payload.setObjectName("payload")
        payload.resize(604, 765)
        payload.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        self.centralwidget = QtWidgets.QWidget(payload)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setObjectName("groupBox")
        self.groupBox_2 = QtWidgets.QGroupBox(self.groupBox)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 80, 561, 101))
        self.groupBox_2.setObjectName("groupBox_2")
        self.layoutWidget = QtWidgets.QWidget(self.groupBox_2)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 30, 211, 23))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_3 = QtWidgets.QLabel(self.layoutWidget)
        self.label_3.setMinimumSize(QtCore.QSize(100, 0))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_4.addWidget(self.label_3)
        self.stationType = QtWidgets.QLineEdit(self.layoutWidget)
        self.stationType.setObjectName("stationType")
        self.horizontalLayout_4.addWidget(self.stationType)
        self.layoutWidget1 = QtWidgets.QWidget(self.groupBox_2)
        self.layoutWidget1.setGeometry(QtCore.QRect(20, 60, 211, 23))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_5 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_5.setMinimumSize(QtCore.QSize(100, 0))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_6.addWidget(self.label_5)
        self.overlayVersion = QtWidgets.QLineEdit(self.layoutWidget1)
        self.overlayVersion.setObjectName("overlayVersion")
        self.horizontalLayout_6.addWidget(self.overlayVersion)
        self.layoutWidget2 = QtWidgets.QWidget(self.groupBox_2)
        self.layoutWidget2.setGeometry(QtCore.QRect(241, 30, 309, 25))
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.layoutWidget2)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_4 = QtWidgets.QLabel(self.layoutWidget2)
        self.label_4.setMinimumSize(QtCore.QSize(100, 0))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_5.addWidget(self.label_4)
        self.limitsVersion = QtWidgets.QLineEdit(self.layoutWidget2)
        self.limitsVersion.setObjectName("limitsVersion")
        self.horizontalLayout_5.addWidget(self.limitsVersion)
        self.stationCount = QtWidgets.QLCDNumber(self.layoutWidget2)
        self.stationCount.setObjectName("stationCount")
        self.horizontalLayout_5.addWidget(self.stationCount)
        self.layoutWidget3 = QtWidgets.QWidget(self.groupBox_2)
        self.layoutWidget3.setGeometry(QtCore.QRect(241, 60, 306, 33))
        self.layoutWidget3.setObjectName("layoutWidget3")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.layoutWidget3)
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_6 = QtWidgets.QLabel(self.layoutWidget3)
        self.label_6.setMinimumSize(QtCore.QSize(100, 0))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_7.addWidget(self.label_6)
        self.selectAll = QtWidgets.QLineEdit(self.layoutWidget3)
        self.selectAll.setObjectName("selectAll")
        self.horizontalLayout_7.addWidget(self.selectAll)
        self.addStation = QtWidgets.QPushButton(self.layoutWidget3)
        self.addStation.setMinimumSize(QtCore.QSize(64, 0))
        self.addStation.setObjectName("addStation")
        self.horizontalLayout_7.addWidget(self.addStation)
        self.groupBox_3 = QtWidgets.QGroupBox(self.groupBox)
        self.groupBox_3.setGeometry(QtCore.QRect(10, 600, 561, 105))
        self.groupBox_3.setObjectName("groupBox_3")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox_3)
        self.gridLayout.setObjectName("gridLayout")
        self.commandShow = QtWidgets.QLineEdit(self.groupBox_3)
        self.commandShow.setObjectName("commandShow")
        self.gridLayout.addWidget(self.commandShow, 0, 0, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 0, 1, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(self.groupBox_3)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 1, 0, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 1, 1, 1, 1)
        self.layoutWidget4 = QtWidgets.QWidget(self.groupBox)
        self.layoutWidget4.setGeometry(QtCore.QRect(10, 30, 221, 23))
        self.layoutWidget4.setObjectName("layoutWidget4")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.layoutWidget4)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(self.layoutWidget4)
        self.label.setMinimumSize(QtCore.QSize(120, 0))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.siteName = QtWidgets.QLineEdit(self.layoutWidget4)
        self.siteName.setReadOnly(True)
        self.siteName.setObjectName("siteName")
        self.horizontalLayout_2.addWidget(self.siteName)
        self.layoutWidget5 = QtWidgets.QWidget(self.groupBox)
        self.layoutWidget5.setGeometry(QtCore.QRect(10, 60, 221, 23))
        self.layoutWidget5.setObjectName("layoutWidget5")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.layoutWidget5)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_2 = QtWidgets.QLabel(self.layoutWidget5)
        self.label_2.setMinimumSize(QtCore.QSize(120, 0))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        self.auditOnly = QtWidgets.QLineEdit(self.layoutWidget5)
        self.auditOnly.setObjectName("auditOnly")
        self.horizontalLayout_3.addWidget(self.auditOnly)
        self.layoutWidget6 = QtWidgets.QWidget(self.groupBox)
        self.layoutWidget6.setGeometry(QtCore.QRect(10, 180, 231, 23))
        self.layoutWidget6.setObjectName("layoutWidget6")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.layoutWidget6)
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label_7 = QtWidgets.QLabel(self.layoutWidget6)
        self.label_7.setMinimumSize(QtCore.QSize(120, 0))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_8.addWidget(self.label_7)
        self.dataCategory = QtWidgets.QLineEdit(self.layoutWidget6)
        self.dataCategory.setObjectName("dataCategory")
        self.horizontalLayout_8.addWidget(self.dataCategory)
        self.layoutWidget7 = QtWidgets.QWidget(self.groupBox)
        self.layoutWidget7.setGeometry(QtCore.QRect(10, 210, 561, 76))
        self.layoutWidget7.setObjectName("layoutWidget7")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(self.layoutWidget7)
        self.horizontalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.label_8 = QtWidgets.QLabel(self.layoutWidget7)
        self.label_8.setMinimumSize(QtCore.QSize(120, 0))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_9.addWidget(self.label_8)
        self.requestColumns = QtWidgets.QTextEdit(self.layoutWidget7)
        self.requestColumns.setPlaceholderText("")
        self.requestColumns.setObjectName("requestColumns")
        self.horizontalLayout_9.addWidget(self.requestColumns)
        self.layoutWidget8 = QtWidgets.QWidget(self.groupBox)
        self.layoutWidget8.setGeometry(QtCore.QRect(10, 290, 231, 23))
        self.layoutWidget8.setObjectName("layoutWidget8")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout(self.layoutWidget8)
        self.horizontalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.label_9 = QtWidgets.QLabel(self.layoutWidget8)
        self.label_9.setMinimumSize(QtCore.QSize(120, 0))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_10.addWidget(self.label_9)
        self.textCategory = QtWidgets.QLineEdit(self.layoutWidget8)
        self.textCategory.setObjectName("textCategory")
        self.horizontalLayout_10.addWidget(self.textCategory)
        self.layoutWidget9 = QtWidgets.QWidget(self.groupBox)
        self.layoutWidget9.setGeometry(QtCore.QRect(10, 320, 231, 23))
        self.layoutWidget9.setObjectName("layoutWidget9")
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout(self.layoutWidget9)
        self.horizontalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.label_10 = QtWidgets.QLabel(self.layoutWidget9)
        self.label_10.setMinimumSize(QtCore.QSize(120, 0))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_11.addWidget(self.label_10)
        self.passFailCategory = QtWidgets.QLineEdit(self.layoutWidget9)
        self.passFailCategory.setObjectName("passFailCategory")
        self.horizontalLayout_11.addWidget(self.passFailCategory)
        self.layoutWidget10 = QtWidgets.QWidget(self.groupBox)
        self.layoutWidget10.setGeometry(QtCore.QRect(10, 350, 231, 23))
        self.layoutWidget10.setObjectName("layoutWidget10")
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout(self.layoutWidget10)
        self.horizontalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.label_11 = QtWidgets.QLabel(self.layoutWidget10)
        self.label_11.setMinimumSize(QtCore.QSize(120, 0))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")
        self.horizontalLayout_12.addWidget(self.label_11)
        self.nullIncluded = QtWidgets.QLineEdit(self.layoutWidget10)
        self.nullIncluded.setObjectName("nullIncluded")
        self.horizontalLayout_12.addWidget(self.nullIncluded)
        self.layoutWidget11 = QtWidgets.QWidget(self.groupBox)
        self.layoutWidget11.setGeometry(QtCore.QRect(10, 380, 231, 23))
        self.layoutWidget11.setObjectName("layoutWidget11")
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout(self.layoutWidget11)
        self.horizontalLayout_13.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.label_12 = QtWidgets.QLabel(self.layoutWidget11)
        self.label_12.setMinimumSize(QtCore.QSize(120, 0))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_12.setFont(font)
        self.label_12.setObjectName("label_12")
        self.horizontalLayout_13.addWidget(self.label_12)
        self.samplePercent = QtWidgets.QLineEdit(self.layoutWidget11)
        self.samplePercent.setObjectName("samplePercent")
        self.horizontalLayout_13.addWidget(self.samplePercent)
        self.layoutWidget12 = QtWidgets.QWidget(self.groupBox)
        self.layoutWidget12.setGeometry(QtCore.QRect(10, 410, 293, 26))
        self.layoutWidget12.setObjectName("layoutWidget12")
        self.horizontalLayout_14 = QtWidgets.QHBoxLayout(self.layoutWidget12)
        self.horizontalLayout_14.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        self.label_13 = QtWidgets.QLabel(self.layoutWidget12)
        self.label_13.setMinimumSize(QtCore.QSize(120, 0))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_13.setFont(font)
        self.label_13.setObjectName("label_13")
        self.horizontalLayout_14.addWidget(self.label_13)
        self.startTime = QtWidgets.QDateTimeEdit(self.layoutWidget12)
        self.startTime.setDateTime(QtCore.QDateTime(QtCore.QDate(2018, 1, 1), QtCore.QTime(0, 0, 0)))
        self.startTime.setDate(QtCore.QDate(2018, 1, 1))
        self.startTime.setObjectName("startTime")
        self.horizontalLayout_14.addWidget(self.startTime)
        self.layoutWidget13 = QtWidgets.QWidget(self.groupBox)
        self.layoutWidget13.setGeometry(QtCore.QRect(10, 440, 293, 26))
        self.layoutWidget13.setObjectName("layoutWidget13")
        self.horizontalLayout_15 = QtWidgets.QHBoxLayout(self.layoutWidget13)
        self.horizontalLayout_15.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_15.setObjectName("horizontalLayout_15")
        self.label_14 = QtWidgets.QLabel(self.layoutWidget13)
        self.label_14.setMinimumSize(QtCore.QSize(120, 0))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_14.setFont(font)
        self.label_14.setObjectName("label_14")
        self.horizontalLayout_15.addWidget(self.label_14)
        self.endTime = QtWidgets.QDateTimeEdit(self.layoutWidget13)
        self.endTime.setDate(QtCore.QDate(2018, 1, 1))
        self.endTime.setObjectName("endTime")
        self.horizontalLayout_15.addWidget(self.endTime)
        self.layoutWidget14 = QtWidgets.QWidget(self.groupBox)
        self.layoutWidget14.setGeometry(QtCore.QRect(10, 470, 231, 23))
        self.layoutWidget14.setObjectName("layoutWidget14")
        self.horizontalLayout_16 = QtWidgets.QHBoxLayout(self.layoutWidget14)
        self.horizontalLayout_16.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_16.setObjectName("horizontalLayout_16")
        self.label_15 = QtWidgets.QLabel(self.layoutWidget14)
        self.label_15.setMinimumSize(QtCore.QSize(120, 0))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_15.setFont(font)
        self.label_15.setObjectName("label_15")
        self.horizontalLayout_16.addWidget(self.label_15)
        self.frequency = QtWidgets.QLineEdit(self.layoutWidget14)
        self.frequency.setObjectName("frequency")
        self.horizontalLayout_16.addWidget(self.frequency)
        self.layoutWidget15 = QtWidgets.QWidget(self.groupBox)
        self.layoutWidget15.setGeometry(QtCore.QRect(10, 500, 231, 23))
        self.layoutWidget15.setObjectName("layoutWidget15")
        self.horizontalLayout_17 = QtWidgets.QHBoxLayout(self.layoutWidget15)
        self.horizontalLayout_17.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_17.setObjectName("horizontalLayout_17")
        self.label_16 = QtWidgets.QLabel(self.layoutWidget15)
        self.label_16.setMinimumSize(QtCore.QSize(120, 0))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_16.setFont(font)
        self.label_16.setObjectName("label_16")
        self.horizontalLayout_17.addWidget(self.label_16)
        self.productCode = QtWidgets.QLineEdit(self.layoutWidget15)
        self.productCode.setObjectName("productCode")
        self.horizontalLayout_17.addWidget(self.productCode)
        self.layoutWidget16 = QtWidgets.QWidget(self.groupBox)
        self.layoutWidget16.setGeometry(QtCore.QRect(10, 530, 561, 76))
        self.layoutWidget16.setObjectName("layoutWidget16")
        self.horizontalLayout_18 = QtWidgets.QHBoxLayout(self.layoutWidget16)
        self.horizontalLayout_18.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_18.setObjectName("horizontalLayout_18")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_17 = QtWidgets.QLabel(self.layoutWidget16)
        self.label_17.setMinimumSize(QtCore.QSize(120, 0))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_17.setFont(font)
        self.label_17.setObjectName("label_17")
        self.verticalLayout.addWidget(self.label_17)
        self.openFile = QtWidgets.QPushButton(self.layoutWidget16)
        self.openFile.setObjectName("openFile")
        self.verticalLayout.addWidget(self.openFile)
        self.horizontalLayout_18.addLayout(self.verticalLayout)
        self.serialNumber = QtWidgets.QTextEdit(self.layoutWidget16)
        self.serialNumber.setObjectName("serialNumber")
        self.horizontalLayout_18.addWidget(self.serialNumber)
        self.layoutWidget17 = QtWidgets.QWidget(self.groupBox)
        self.layoutWidget17.setGeometry(QtCore.QRect(330, 710, 241, 32))
        self.layoutWidget17.setObjectName("layoutWidget17")
        self.horizontalLayout_19 = QtWidgets.QHBoxLayout(self.layoutWidget17)
        self.horizontalLayout_19.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_19.setObjectName("horizontalLayout_19")
        self.cancel = QtWidgets.QPushButton(self.layoutWidget17)
        self.cancel.setMinimumSize(QtCore.QSize(100, 0))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.cancel.setFont(font)
        self.cancel.setObjectName("cancel")
        self.horizontalLayout_19.addWidget(self.cancel)
        spacerItem = QtWidgets.QSpacerItem(18, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_19.addItem(spacerItem)
        self.confirm = QtWidgets.QPushButton(self.layoutWidget17)
        self.confirm.setMinimumSize(QtCore.QSize(100, 0))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.confirm.setFont(font)
        self.confirm.setObjectName("confirm")
        self.horizontalLayout_19.addWidget(self.confirm)
        self.widget = QtWidgets.QWidget(self.groupBox)
        self.widget.setGeometry(QtCore.QRect(300, 290, 221, 23))
        self.widget.setObjectName("widget")
        self.horizontalLayout_20 = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout_20.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_20.setObjectName("horizontalLayout_20")
        self.label_18 = QtWidgets.QLabel(self.widget)
        self.label_18.setMinimumSize(QtCore.QSize(100, 0))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_18.setFont(font)
        self.label_18.setObjectName("label_18")
        self.horizontalLayout_20.addWidget(self.label_18)
        self.modules = QtWidgets.QLineEdit(self.widget)
        self.modules.setObjectName("modules")
        self.horizontalLayout_20.addWidget(self.modules)
        self.widget1 = QtWidgets.QWidget(self.groupBox)
        self.widget1.setGeometry(QtCore.QRect(300, 320, 221, 23))
        self.widget1.setObjectName("widget1")
        self.horizontalLayout_21 = QtWidgets.QHBoxLayout(self.widget1)
        self.horizontalLayout_21.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_21.setObjectName("horizontalLayout_21")
        self.label_19 = QtWidgets.QLabel(self.widget1)
        self.label_19.setMinimumSize(QtCore.QSize(100, 0))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_19.setFont(font)
        self.label_19.setObjectName("label_19")
        self.horizontalLayout_21.addWidget(self.label_19)
        self.attributes = QtWidgets.QLineEdit(self.widget1)
        self.attributes.setObjectName("attributes")
        self.horizontalLayout_21.addWidget(self.attributes)
        self.horizontalLayout.addWidget(self.groupBox)
        payload.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(payload)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 608, 22))
        self.menubar.setObjectName("menubar")
        payload.setMenuBar(self.menubar)

        self.retranslateUi(payload)

        self.cancel.clicked.connect(self.cancelButton)
        self.confirm.clicked.connect(self.confirmButton)
        self.addStation.clicked.connect(self.addStationButton)
        self.openFile.clicked.connect(self.openFileButton)
        self.pushButton.clicked.connect(self.cmdReplaceButton)
        self.pushButton_2.clicked.connect(self.cfgReplaceButton)

        QtCore.QMetaObject.connectSlotsByName(payload)

    def retranslateUi(self, payload):
        _translate = QtCore.QCoreApplication.translate
        payload.setWindowTitle(_translate("payload", "MainWindow"))
        self.groupBox.setTitle(_translate("payload", "payload"))
        self.groupBox_2.setTitle(_translate("payload", "parametricType"))
        self.label_3.setText(_translate("payload", "stationType"))
        self.label_5.setText(_translate("payload", "overlayVersion"))
        self.label_4.setText(_translate("payload", "limitsVersion"))
        self.label_6.setText(_translate("payload", "selectAll"))
        self.selectAll.setText(_translate("payload", "true"))
        self.addStation.setText(_translate("payload", "ADD"))
        self.groupBox_3.setTitle(_translate("payload", "command - config"))
        self.pushButton.setText(_translate("payload", "cmd - replace"))
        self.pushButton_2.setText(_translate("payload", "cfg - replace"))
        self.label.setText(_translate("payload", "siteName"))
        self.siteName.setText(_translate("payload", "QSMC"))
        self.label_2.setText(_translate("payload", "auditOnly"))
        self.auditOnly.setText(_translate("payload", "Y"))
        self.label_7.setText(_translate("payload", "dataCategory"))
        self.dataCategory.setText(_translate("payload", "pdata"))
        self.label_8.setText(_translate("payload", "requestdColumns"))
        self.requestColumns.setHtml(_translate("payload",
                                               "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                               "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                               "p, li { white-space: pre-wrap; }\n"
                                               "</style></head><body style=\" font-family:\'.SF NS Text\'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
                                               "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">siteName,productCode,serialNumber,specialBuildName,specialBuildDescription,unitNumber,stationId,testResult,startTestTime,endTestTime,overlayVersion,listOfFailingTests</p></body></html>"))
        self.label_9.setText(_translate("payload", "textCategory"))
        self.textCategory.setText(_translate("payload", "All"))
        self.label_10.setText(_translate("payload", "passFailCategory"))
        self.passFailCategory.setText(_translate("payload", "All"))
        self.label_11.setText(_translate("payload", "nullIncluded"))
        self.nullIncluded.setText(_translate("payload", "N"))
        self.label_12.setText(_translate("payload", "samplePercent"))
        self.samplePercent.setText(_translate("payload", "100"))
        self.label_13.setText(_translate("payload", "startTime"))
        self.startTime.setDisplayFormat(_translate("payload", "yyyy-MM-dd hh:mm:ss"))
        self.label_14.setText(_translate("payload", "endTime"))
        self.endTime.setDisplayFormat(_translate("payload", "yyyy-MM-dd hh:mm:ss"))
        self.label_15.setText(_translate("payload", "frequency"))
        self.frequency.setText(_translate("payload", "now"))
        self.label_16.setText(_translate("payload", "productCode"))
        self.label_17.setText(_translate("payload", "serialNumber"))
        self.openFile.setText(_translate("payload", "Open File"))
        self.cancel.setText(_translate("payload", "cancel"))
        self.confirm.setText(_translate("payload", "confirm"))
        self.label_18.setText(_translate("payload", "modules"))
        self.modules.setText(_translate("payload", "N"))
        self.label_19.setText(_translate("payload", "attributes"))
        self.attributes.setText(_translate("payload", "N"))