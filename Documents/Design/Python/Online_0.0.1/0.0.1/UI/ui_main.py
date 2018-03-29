#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time     : 2018/3/8下午3:01
# @Author   : Saseny Zhou
# @Site     : 
# @File     : ui_main.py
# @Software : PyCharm


from PyQt5 import QtCore, QtGui, QtWidgets
from Path.path import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 820)
        MainWindow.setDocumentMode(False)
        MainWindow.setDockNestingEnabled(False)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralWidget)
        self.horizontalLayout.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.productList = QtWidgets.QListWidget(self.centralWidget)
        self.productList.setObjectName("productList")
        self.horizontalLayout.addWidget(self.productList)
        self.stationList = QtWidgets.QListWidget(self.centralWidget)
        self.stationList.setObjectName("stationList")
        self.horizontalLayout.addWidget(self.stationList)
        self.chooseList = QtWidgets.QListWidget(self.centralWidget)
        self.chooseList.setObjectName("chooseList")
        self.horizontalLayout.addWidget(self.chooseList)
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 769, 22))
        self.menuBar.setObjectName("menuBar")
        MainWindow.setMenuBar(self.menuBar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setMovable(True)
        self.toolBar.setAllowedAreas(QtCore.Qt.AllToolBarAreas)
        self.toolBar.setOrientation(QtCore.Qt.Horizontal)
        self.toolBar.setIconSize(QtCore.QSize(15, 15))
        self.toolBar.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.toolBar.setFloatable(True)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionUser = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(imagePath + "/user_off.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionUser.setIcon(icon)
        self.actionUser.setIconVisibleInMenu(False)
        self.actionUser.setObjectName("actionUser")
        self.actionopen = QtWidgets.QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(imagePath + "/open.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionopen.setIcon(icon1)
        self.actionopen.setObjectName("actionopen")
        self.actionhome = QtWidgets.QAction(MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(imagePath + "/home.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionhome.setIcon(icon2)
        self.actionhome.setObjectName("actionhome")
        self.actionrun = QtWidgets.QAction(MainWindow)
        self.actionrun.setCheckable(False)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(imagePath + "/running.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionrun.setIcon(icon3)
        self.actionrun.setObjectName("actionrun")
        self.toolBar.addAction(self.actionhome)
        self.toolBar.addAction(self.actionopen)
        self.toolBar.addAction(self.actionUser)
        self.toolBar.addAction(self.actionrun)

        self.actionhome.triggered.connect(self.homeSet)
        self.actionopen.triggered.connect(self.openFile)
        self.actionUser.triggered.connect(self.loginUser)
        self.actionrun.triggered.connect(self.running)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Tools"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.actionUser.setText(_translate("MainWindow", "user"))
        self.actionUser.setToolTip(_translate("MainWindow", "administer"))
        self.actionUser.setShortcut(_translate("MainWindow", "Meta+U"))
        self.actionopen.setText(_translate("MainWindow", "open"))
        self.actionopen.setToolTip(_translate("MainWindow", "open result"))
        self.actionopen.setShortcut(_translate("MainWindow", "Meta+O"))
        self.actionhome.setText(_translate("MainWindow", "home"))
        self.actionhome.setToolTip(_translate("MainWindow", "home setup"))
        self.actionhome.setShortcut(_translate("MainWindow", "Meta+H"))
        self.actionrun.setText(_translate("MainWindow", "run"))
        self.actionrun.setToolTip(_translate("MainWindow", "run"))
        self.actionrun.setShortcut(_translate("MainWindow", "Meta+R"))
