#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time     : 2018/3/8下午3:03
# @Author   : Saseny Zhou
# @Site     : 
# @File     : ui_running.py
# @Software : PyCharm

from PyQt5 import QtCore, QtGui, QtWidgets
from Path.path import *


class Ui_running(object):
    def setupUi(self, running):
        running.setObjectName("running")
        running.resize(1300, 700)
        self.centralwidget = QtWidgets.QWidget(running)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.logCheck = QtWidgets.QPushButton(self.centralwidget)
        self.logCheck.setAutoFillBackground(False)
        self.logCheck.setCheckable(False)
        self.logCheck.setAutoDefault(False)
        self.logCheck.setObjectName("logCheck")
        self.gridLayout.addWidget(self.logCheck, 1, 1, 1, 1)
        self.logAppend = QtWidgets.QTextEdit(self.centralwidget)
        self.logAppend.setReadOnly(True)
        self.logAppend.setObjectName("logAppend")
        self.gridLayout.addWidget(self.logAppend, 0, 1, 1, 1)
        self.statesCheck = QtWidgets.QTableWidget(self.centralwidget)
        self.statesCheck.setMaximumSize(QtCore.QSize(500, 16777215))
        self.statesCheck.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.statesCheck.setAlternatingRowColors(True)
        self.statesCheck.setObjectName("statesCheck")
        self.statesCheck.setColumnCount(2)
        self.statesCheck.setRowCount(100)

        for i in range(100):
            item = QtWidgets.QTableWidgetItem()
            self.statesCheck.setVerticalHeaderItem(i, item)

        item = QtWidgets.QTableWidgetItem()
        self.statesCheck.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.statesCheck.setHorizontalHeaderItem(1, item)
        self.statesCheck.horizontalHeader().setSortIndicatorShown(False)
        self.statesCheck.horizontalHeader().setStretchLastSection(True)
        self.gridLayout.addWidget(self.statesCheck, 0, 0, 2, 1)
        running.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(running)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 757, 22))
        self.menubar.setObjectName("menubar")
        running.setMenuBar(self.menubar)

        self.retranslateUi(running)
        self.statesCheck.setColumnWidth(0, 200)
        self.logCheck.clicked.connect(self.logCheckButton)
        QtCore.QMetaObject.connectSlotsByName(running)

    def retranslateUi(self, running):
        _translate = QtCore.QCoreApplication.translate
        running.setWindowTitle(_translate("running", "Runing"))
        self.logCheck.setText(_translate("running", "Check Log"))
        self.logCheck.setShortcut(_translate("running", "L"))
        item = self.statesCheck.horizontalHeaderItem(0)
        item.setText(_translate("running", "Station"))
        item = self.statesCheck.horizontalHeaderItem(1)
        item.setText(_translate("running", "States"))
