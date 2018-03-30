#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time     : 2018/2/8下午1:16
# @Author   : Saseny Zhou
# @Site     : 
# @File     : ui_running.py
# @Software : PyCharm


from PyQt5 import QtCore, QtGui, QtWidgets
from functions.path import *


class Ui_Running(object):
    def setupUi(self, Running):
        Running.setObjectName("Running")
        Running.resize(900, 429)
        self.centralwidget = QtWidgets.QWidget(Running)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setMaximumSize(QtCore.QSize(500, 400))
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(30)
        for i in range(30):
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget.setVerticalHeaderItem(i, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        self.tableWidget.horizontalHeader().setSortIndicatorShown(False)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.horizontalLayout.addWidget(self.tableWidget)
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName("textEdit")
        self.horizontalLayout.addWidget(self.textEdit)
        Running.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Running)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 811, 22))
        self.menubar.setObjectName("menubar")
        Running.setMenuBar(self.menubar)

        self.tableWidget.setColumnWidth(0, 170)

        self.retranslateUi(Running)
        QtCore.QMetaObject.connectSlotsByName(Running)

    def retranslateUi(self, Running):
        _translate = QtCore.QCoreApplication.translate
        Running.setWindowTitle(_translate("Running", "Running"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Running", "Station"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Running", "States"))
