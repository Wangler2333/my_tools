#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time     : 2018/3/16下午12:22
# @Author   : Saseny Zhou
# @Site     : 
# @File     : ui_search.py
# @Software : PyCharm

from PyQt5 import QtCore, QtGui, QtWidgets
from Path.path import *


class Ui_search(object):
    def setupUi(self, search):
        search.setObjectName("search")
        search.resize(500, 538)
        search.setStyleSheet("font: 25 14pt \"STFangsong\";")
        self.centralwidget = QtWidgets.QWidget(search)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setObjectName("comboBox")
        self.horizontalLayout.addWidget(self.comboBox)
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("STFangsong")
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(3)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.lineEdit_4 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_4.setStyleSheet("background-color: rgb(239, 255, 228);")
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.gridLayout.addWidget(self.lineEdit_4, 2, 2, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 3, 1, 1)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_2.setStyleSheet("background-color: rgb(254, 240, 255);")
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.gridLayout.addWidget(self.lineEdit_2, 0, 2, 1, 1)
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setMinimumSize(QtCore.QSize(70, 0))
        self.label.setMaximumSize(QtCore.QSize(70, 16777215))
        font = QtGui.QFont()
        font.setFamily("STFangsong")
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(3)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 2)
        self.lineEdit_3 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_3.setStyleSheet("background-color: rgb(227, 255, 255);")
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.gridLayout.addWidget(self.lineEdit_3, 1, 2, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setMinimumSize(QtCore.QSize(70, 0))
        self.label_3.setMaximumSize(QtCore.QSize(70, 16777215))
        font = QtGui.QFont()
        font.setFamily("STFangsong")
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(3)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setMinimumSize(QtCore.QSize(70, 0))
        self.label_2.setMaximumSize(QtCore.QSize(70, 16777215))
        font = QtGui.QFont()
        font.setFamily("STFangsong")
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(3)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 2)
        self.verticalLayout.addWidget(self.groupBox)
        self.columnView = QtWidgets.QListWidget(self.centralwidget)
        self.columnView.setObjectName("columnView")
        self.verticalLayout.addWidget(self.columnView)
        search.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(search)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 453, 22))
        self.menubar.setObjectName("menubar")
        search.setMenuBar(self.menubar)

        self.retranslateUi(search)
        self.lineEdit_2.setReadOnly(True)
        self.lineEdit_3.setReadOnly(True)
        self.lineEdit_4.setReadOnly(True)
        self.pushButton.clicked.connect(self.search)
        self.lineEdit.returnPressed.connect(self.pushButton.click)
        QtCore.QMetaObject.connectSlotsByName(search)

    def retranslateUi(self, search):
        _translate = QtCore.QCoreApplication.translate
        search.setWindowTitle(_translate("search", "机器信息搜索"))
        self.pushButton.setText(_translate("search", "搜索"))
        self.label.setText(_translate("search", "序列号:"))
        self.label_3.setText(_translate("search", "Config:"))
        self.label_2.setText(_translate("search", "机器号:"))