#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time     : 2018/2/20下午1:00
# @Author   : Saseny Zhou
# @Site     : 
# @File     : ui_change.py
# @Software : PyCharm


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_change(object):
    def setupUi(self, change):
        change.setObjectName("change")
        change.resize(277, 193)
        self.centralwidget = QtWidgets.QWidget(change)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setMinimumSize(QtCore.QSize(200, 100))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton_3 = QtWidgets.QPushButton(self.groupBox)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setObjectName("pushButton_3")
        self.gridLayout.addWidget(self.pushButton_3, 1, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(self.groupBox)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 0, 1, 1, 1)
        self.verticalLayout.addWidget(self.groupBox)
        change.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(change)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 277, 22))
        self.menubar.setObjectName("menubar")
        change.setMenuBar(self.menubar)

        self.pushButton.clicked.connect(self.delete_choose)
        self.pushButton_2.clicked.connect(self.change_command)
        self.pushButton_3.clicked.connect(self.change_config)

        self.retranslateUi(change)
        QtCore.QMetaObject.connectSlotsByName(change)

    def retranslateUi(self, change):
        _translate = QtCore.QCoreApplication.translate
        change.setWindowTitle(_translate("change", "MainWindow"))
        self.label.setText(_translate("change", "Delete Item ?"))
        self.pushButton.setText(_translate("change", "Yes"))
        self.pushButton_3.setText(_translate("change", "Confirm"))
        self.label_3.setText(_translate("change", "Replace Config"))
        self.label_2.setText(_translate("change", "Replace Command"))
        self.pushButton_2.setText(_translate("change", "Confirm"))
