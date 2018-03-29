#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time     : 2018/3/8下午3:04
# @Author   : Saseny Zhou
# @Site     : 
# @File     : delete.py
# @Software : PyCharm

from PyQt5.QtWidgets import *
from UI.ui_delete import *
from PyQt5.QtCore import *


class DeleteConfirm(QMainWindow, Ui_DeleteConfirm):
    confirmSignal = pyqtSignal(dict)

    def __init__(self, info):
        super(DeleteConfirm, self).__init__()
        self.setupUi(self)
        self.center()
        self.setWindowFlags(QtCore.Qt.CustomizeWindowHint | QtCore.Qt.FramelessWindowHint)
        self.info = info
        self.label.setText("Whether Delete Station: {}".format(self.info))

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def confirm(self):
        self.confirmSignal.emit({"station": self.info, "confirm": True})
        self.close()

    def cancel(self):
        self.confirmSignal.emit({"station": self.info, "confirm": False})
        self.close()
