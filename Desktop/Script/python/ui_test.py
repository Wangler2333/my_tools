# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/sasenyzhou/Qt_Project/MyApp/myapp.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *


class Ui_MyApp(object):
    def setupUi(self, MyApp):
        MyApp.setObjectName("MyApp")
        MyApp.resize(1159, 867)
        font = QtGui.QFont()
        font.setFamily("BiauKai")
        font.setPointSize(13)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        MyApp.setFont(font)
        self.centralWidget = QtWidgets.QWidget(MyApp)
        self.centralWidget.setObjectName("centralWidget")
        self.lineEdit = QtWidgets.QLineEdit(self.centralWidget)
        self.lineEdit.setGeometry(QtCore.QRect(30, 30, 471, 21))
        font = QtGui.QFont()
        font.setFamily(".SF NS Text")
        self.lineEdit.setFont(font)
        self.lineEdit.setObjectName("lineEdit")
        MyApp.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(MyApp)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1159, 22))
        self.menuBar.setObjectName("menuBar")
        MyApp.setMenuBar(self.menuBar)
        self.statusBar = QtWidgets.QStatusBar(MyApp)
        self.statusBar.setObjectName("statusBar")
        MyApp.setStatusBar(self.statusBar)

        self.retranslateUi(MyApp)
        self.lineEdit.selectionChanged.connect(self.button)
        QtCore.QMetaObject.connectSlotsByName(MyApp)

    def retranslateUi(self, MyApp):
        _translate = QtCore.QCoreApplication.translate
        MyApp.setWindowTitle(_translate("MyApp", "MyApp"))

    def button(self):
        file, type = QFileDialog.getOpenFileName(self, "选取文件", "/", "CSV Files (*.csv);;Text Files (*.txt)")
        if file:
            self.lineEdit.setText(file)
