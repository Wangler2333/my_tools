#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time     : 2018/3/8下午2:27
# @Author   : Saseny Zhou
# @Site     : 
# @File     : ui_home.py
# @Software : PyCharm


from PyQt5 import QtCore, QtGui, QtWidgets
from Path.path import *


class Ui_Home(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(335, 80)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(10, 10, 316, 32))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setMinimumSize(QtCore.QSize(194, 0))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.pushButton = QtWidgets.QPushButton(self.widget)
        self.pushButton.setMinimumSize(QtCore.QSize(110, 0))
        self.pushButton.setMaximumSize(QtCore.QSize(110, 16777215))
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.widget1 = QtWidgets.QWidget(self.centralwidget)
        self.widget1.setGeometry(QtCore.QRect(10, 40, 316, 33))
        self.widget1.setObjectName("widget1")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget1)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.tokenID = QtWidgets.QLineEdit(self.widget1)
        self.tokenID.setMinimumSize(QtCore.QSize(200, 0))
        self.tokenID.setObjectName("tokenID")
        self.horizontalLayout_2.addWidget(self.tokenID)
        self.pushButton_2 = QtWidgets.QPushButton(self.widget1)
        self.pushButton_2.setMinimumSize(QtCore.QSize(110, 0))
        self.pushButton_2.setMaximumSize(QtCore.QSize(110, 16777215))
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout_2.addWidget(self.pushButton_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 335, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)

        self.pushButton.clicked.connect(self.loadConfig)
        self.pushButton_2.clicked.connect(self.changeToken)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "HOME"))
        self.label.setText(_translate("MainWindow", "Load  Comm  Config   "))
        self.pushButton.setText(_translate("MainWindow", "Load"))
        self.tokenID.setPlaceholderText(_translate("MainWindow", "Input token"))
        self.pushButton_2.setText(_translate("MainWindow", "Change"))
