#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time     : 2018/2/20下午1:00
# @Author   : Saseny Zhou
# @Site     : 
# @File     : change.py
# @Software : PyCharm


from UI.ui_change import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class ChangeSet(QMainWindow, Ui_change):
    delete_signal = pyqtSignal(dict)

    def __init__(self, product):
        super(ChangeSet, self).__init__()
        self.setupUi(self)
        self.return_dict = {
            "delete": False,
            "command": False,
            "config": False,
            "product": product
        }

    def delete_choose(self):
        self.return_dict["delete"] = True
        self.delete_signal.emit(self.return_dict)
        self.close()

    def change_command(self):
        self.return_dict["command"] = True
        self.delete_signal.emit(self.return_dict)
        self.return_dict["command"] = False

    def change_config(self):
        self.return_dict["config"] = True
        self.delete_signal.emit(self.return_dict)
        self.return_dict["config"] = False
