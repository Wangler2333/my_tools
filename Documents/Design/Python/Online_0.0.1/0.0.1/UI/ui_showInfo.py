#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time     : 2018/3/8下午3:02
# @Author   : Saseny Zhou
# @Site     : 
# @File     : ui_showInfo.py
# @Software : PyCharm

from PyQt5 import QtCore, QtGui, QtWidgets
from Path.path import *


class Ui_show(object):
    def setupUi(self, show):
        show.setObjectName("show")
        show.resize(404, 421)
        self.centralwidget = QtWidgets.QWidget(show)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName("textEdit")
        self.horizontalLayout.addWidget(self.textEdit)
        show.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(show)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 404, 22))
        self.menubar.setObjectName("menubar")
        show.setMenuBar(self.menubar)

        self.retranslateUi(show)
        QtCore.QMetaObject.connectSlotsByName(show)

    def retranslateUi(self, show):
        _translate = QtCore.QCoreApplication.translate
        show.setWindowTitle(_translate("show", "ShowInfo"))
