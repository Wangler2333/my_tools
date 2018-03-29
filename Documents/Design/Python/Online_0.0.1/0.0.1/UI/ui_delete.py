#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time     : 2018/3/8下午3:02
# @Author   : Saseny Zhou
# @Site     : 
# @File     : ui_delete.py
# @Software : PyCharm


from PyQt5 import QtCore, QtGui, QtWidgets
from Path.path import *


class Ui_DeleteConfirm(object):
    def setupUi(self, DeleteConfirm):
        DeleteConfirm.setObjectName("DeleteConfirm")
        DeleteConfirm.resize(314, 138)
        DeleteConfirm.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        self.centralwidget = QtWidgets.QWidget(DeleteConfirm)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setStyleSheet("background-color: rgb(252, 51, 42);")
        self.label.setFrameShape(QtWidgets.QFrame.Panel)
        self.label.setFrameShadow(QtWidgets.QFrame.Raised)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 2)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setMinimumSize(QtCore.QSize(0, 45))
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 1, 0, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setMinimumSize(QtCore.QSize(0, 45))
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 1, 1, 1, 1)
        DeleteConfirm.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(DeleteConfirm)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 314, 22))
        self.menubar.setObjectName("menubar")
        DeleteConfirm.setMenuBar(self.menubar)

        self.retranslateUi(DeleteConfirm)
        self.pushButton_2.clicked.connect(self.confirm)
        self.pushButton.clicked.connect(self.cancel)
        QtCore.QMetaObject.connectSlotsByName(DeleteConfirm)

    def retranslateUi(self, DeleteConfirm):
        _translate = QtCore.QCoreApplication.translate
        DeleteConfirm.setWindowTitle(_translate("DeleteConfirm", "DELETE CONFIRM"))
        self.label.setText(_translate("DeleteConfirm", ""))
        self.pushButton.setText(_translate("DeleteConfirm", "NO"))
        self.pushButton_2.setText(_translate("DeleteConfirm", "YES"))
