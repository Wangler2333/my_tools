# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/saseny/PycharmProjects/Download/Download/download.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *


class Ui_Download(object):
    def setupUi(self, Download):
        Download.setObjectName("Download")
        Download.resize(752, 578)
        self.centralWidget = QtWidgets.QWidget(Download)
        self.centralWidget.setObjectName("centralWidget")
        self.groupBox = QtWidgets.QGroupBox(self.centralWidget)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 731, 381))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.textEdit = QtWidgets.QTextEdit(self.groupBox)
        self.textEdit.setGeometry(QtCore.QRect(10, 30, 171, 301))
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName("textEdit")
        self.textEdit_2 = QtWidgets.QTextEdit(self.groupBox)
        self.textEdit_2.setGeometry(QtCore.QRect(190, 30, 171, 301))
        self.textEdit_2.setReadOnly(True)
        self.textEdit_2.setObjectName("textEdit_2")
        self.textEdit_3 = QtWidgets.QTextEdit(self.groupBox)
        self.textEdit_3.setGeometry(QtCore.QRect(370, 30, 171, 301))
        self.textEdit_3.setReadOnly(True)
        self.textEdit_3.setObjectName("textEdit_3")
        self.textEdit_4 = QtWidgets.QTextEdit(self.groupBox)
        self.textEdit_4.setGeometry(QtCore.QRect(550, 30, 171, 301))
        self.textEdit_4.setReadOnly(True)
        self.textEdit_4.setObjectName("textEdit_4")
        self.lcdNumber = QtWidgets.QLCDNumber(self.groupBox)
        self.lcdNumber.setGeometry(QtCore.QRect(10, 340, 111, 31))
        self.lcdNumber.setObjectName("lcdNumber")
        self.lcdNumber_2 = QtWidgets.QLCDNumber(self.groupBox)
        self.lcdNumber_2.setGeometry(QtCore.QRect(190, 340, 111, 31))
        self.lcdNumber_2.setObjectName("lcdNumber_2")
        self.lcdNumber_5 = QtWidgets.QLCDNumber(self.groupBox)
        self.lcdNumber_5.setGeometry(QtCore.QRect(370, 340, 111, 31))
        self.lcdNumber_5.setObjectName("lcdNumber_5")
        self.lcdNumber_6 = QtWidgets.QLCDNumber(self.groupBox)
        self.lcdNumber_6.setGeometry(QtCore.QRect(550, 340, 111, 31))
        self.lcdNumber_6.setObjectName("lcdNumber_6")
        self.label_6 = QtWidgets.QLabel(self.groupBox)
        self.label_6.setGeometry(QtCore.QRect(10, 10, 60, 16))
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.groupBox)
        self.label_7.setGeometry(QtCore.QRect(190, 10, 60, 16))
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.groupBox)
        self.label_8.setGeometry(QtCore.QRect(370, 10, 60, 16))
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(self.groupBox)
        self.label_9.setGeometry(QtCore.QRect(550, 10, 60, 16))
        self.label_9.setObjectName("label_9")
        self.pushButton_4 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_4.setGeometry(QtCore.QRect(120, 340, 61, 32))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_5 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_5.setGeometry(QtCore.QRect(300, 340, 61, 32))
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_6 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_6.setGeometry(QtCore.QRect(480, 340, 61, 32))
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_7 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_7.setGeometry(QtCore.QRect(660, 340, 61, 32))
        self.pushButton_7.setObjectName("pushButton_7")
        self.line = QtWidgets.QFrame(self.centralWidget)
        self.line.setGeometry(QtCore.QRect(0, 390, 751, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralWidget)
        self.groupBox_2.setGeometry(QtCore.QRect(50, 410, 371, 131))
        self.groupBox_2.setTitle("")
        self.groupBox_2.setObjectName("groupBox_2")
        self.label = QtWidgets.QLabel(self.groupBox_2)
        self.label.setGeometry(QtCore.QRect(10, 15, 111, 21))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.groupBox_2)
        self.label_2.setGeometry(QtCore.QRect(10, 45, 101, 21))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.groupBox_2)
        self.label_3.setGeometry(QtCore.QRect(120, 15, 201, 21))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.groupBox_2)
        self.label_4.setGeometry(QtCore.QRect(120, 45, 201, 21))
        self.label_4.setObjectName("label_4")
        self.pushButton = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton.setGeometry(QtCore.QRect(310, 10, 50, 32))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton_2.setGeometry(QtCore.QRect(310, 40, 50, 32))
        self.pushButton_2.setObjectName("pushButton_2")
        self.lineEdit = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEdit.setGeometry(QtCore.QRect(120, 80, 61, 21))
        self.lineEdit.setAutoFillBackground(False)
        self.lineEdit.setReadOnly(True)
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEdit_2.setGeometry(QtCore.QRect(200, 80, 61, 21))
        self.lineEdit_2.setReadOnly(True)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEdit_3.setGeometry(QtCore.QRect(280, 80, 61, 21))
        self.lineEdit_3.setReadOnly(True)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.label_5 = QtWidgets.QLabel(self.groupBox_2)
        self.label_5.setGeometry(QtCore.QRect(10, 80, 101, 21))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton_3.setGeometry(QtCore.QRect(450, 410, 281, 91))
        self.pushButton_3.setObjectName("pushButton_3")
        self.commandLinkButton = QtWidgets.QCommandLinkButton(self.centralWidget)
        self.commandLinkButton.setGeometry(QtCore.QRect(460, 500, 261, 41))
        self.commandLinkButton.setObjectName("commandLinkButton")

        self.label_10 = QtWidgets.QLabel(self.centralWidget)
        self.label_10.setGeometry(QtCore.QRect(50, 550, 141, 16))
        self.label_10.setObjectName("label_10")
        self.label_11 = QtWidgets.QLabel(self.centralWidget)
        self.label_11.setGeometry(QtCore.QRect(200, 550, 141, 16))
        self.label_11.setObjectName("label_11")
        self.label_12 = QtWidgets.QLabel(self.centralWidget)
        self.label_12.setGeometry(QtCore.QRect(370, 550, 141, 16))
        self.label_12.setObjectName("label_12")
        self.label_13 = QtWidgets.QLabel(self.centralWidget)
        self.label_13.setGeometry(QtCore.QRect(520, 550, 141, 16))
        self.label_13.setObjectName("label_13")

        Download.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(Download)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 752, 22))
        self.menuBar.setObjectName("menuBar")
        Download.setMenuBar(self.menuBar)

        #self.statusBar = QtWidgets.QStatusBar(Download)
        #self.statusBar.setObjectName("statusBar")
        #Download.setStatusBar(self.statusBar)

        self.retranslateUi(Download)
        self.lineEdit.selectionChanged.connect(self.lineEditChange)
        self.lineEdit_2.selectionChanged.connect(self.lineEdit_2Change)
        self.lineEdit_3.selectionChanged.connect(self.lineEdit_3Change)
        self.pushButton.clicked.connect(self.pushButtonClick)
        self.pushButton_2.clicked.connect(self.pushButton_2Click)
        self.pushButton_3.clicked.connect(self.startButton)
        self.pushButton_4.clicked.connect(self.textEdit.clear)
        self.pushButton_5.clicked.connect(self.textEdit_2.clear)
        self.pushButton_6.clicked.connect(self.textEdit_3.clear)
        self.pushButton_7.clicked.connect(self.textEdit_4.clear)
        self.commandLinkButton.clicked.connect(self.commandLinkButtonclick)
        QtCore.QMetaObject.connectSlotsByName(Download)

    def retranslateUi(self, Download):
        _translate = QtCore.QCoreApplication.translate
        Download.setWindowTitle(_translate("Download", "Download"))
        self.label_6.setText(_translate("Download", "Disk1"))
        self.label_7.setText(_translate("Download", "Disk2"))
        self.label_8.setText(_translate("Download", "Disk3"))
        self.label_9.setText(_translate("Download", "Disk4"))
        self.pushButton_4.setText(_translate("Download", "Clear"))
        self.pushButton_5.setText(_translate("Download", "Clear"))
        self.pushButton_6.setText(_translate("Download", "Clear"))
        self.pushButton_7.setText(_translate("Download", "Clear"))
        self.label.setText(_translate("Download", "Test Bundle:"))
        self.label_2.setText(_translate("Download", "CM   Bundle:"))
        self.label_3.setText(_translate("Download", "J79A_Ramp_3-8_18.0B2"))
        self.label_4.setText(_translate("Download", "2Z694-09335"))
        self.pushButton.setText(_translate("Download", "..."))
        self.pushButton_2.setText(_translate("Download", "..."))
        self.lineEdit.setText(_translate("Download", ""))
        self.lineEdit_2.setText(_translate("Download", ""))
        self.lineEdit_3.setText(_translate("Download", ""))
        self.label_5.setText(_translate("Download", "Partition   :"))
        self.pushButton_3.setText(_translate("Download", "DOWNLOAD"))
        self.commandLinkButton.setText(_translate("Download", "eraseDisk Command Link"))