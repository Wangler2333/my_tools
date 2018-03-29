#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time     : 2018/3/8上午10:45
# @Author   : Saseny Zhou
# @Site     : 
# @File     : login.py
# @Software : PyCharm


from UI.ui_login import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from Encrypt.encrypt import *


class LogIn(QMainWindow, Ui_login):
    login_signal = pyqtSignal()

    def __init__(self):
        super(LogIn, self).__init__()
        self.setupUi(self)
        self.center()
        self.count = 0
        self.lineEdit_2.editingFinished.connect(self.loginConfirm)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def loginConfirm(self):
        userName = self.lineEdit.text()
        passWord = self.lineEdit_2.text()

        collectLogs.logger.info("Login UserName: {}".format(userName))
        collectLogs.logger.info("Login PassWord: {}".format("******"))

        if self.count > 2:
            self.close()
        self.count += 1

        collectLogs.logger.info("Login Verify Times: {}".format(self.count))

        if password_verify(userName, passWord) is True:
            collectLogs.logger.debug("UserInfo Verified Passed")
            self.login_signal.emit()
            self.close()
        else:
            collectLogs.logger.debug("UserInfo Verified Failed")

    def re_Input(self):
        collectLogs.logger.info("Click Re-Input Button then clear info")
        self.lineEdit.clear()
        self.lineEdit_2.clear()
