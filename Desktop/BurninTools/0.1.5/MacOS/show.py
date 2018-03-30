#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time   : 3/15/18 10:32 PM
# @Author : Saseny.Zhou
# @File   : show.py


from PyQt5.QtWidgets import *
from UI.ui_show import *
from Path.path import *


class ShowError(QMainWindow, Ui_show_error):
    def __init__(self, info):
        super(ShowError, self).__init__()
        self.setupUi(self)
        # self.setWindowFlags(QtCore.Qt.CustomizeWindowHint | QtCore.Qt.FramelessWindowHint)
        self.info = info
        self.showInfo()

    def showInfo(self):
        serial_number = self.info.get("serial number", "None")
        dti_info = self.info.get("dti info", "None")
        error_code = self.info.get("exist code", "None")
        path_road = self.info.get("folder", "None")
        need_add = self.info.get("need add", "None")


        """数据去重"""
        error_code = [x for x in set(error_code)]
        need_add = [x for x in set(need_add)]
        count = len(need_add)

        print(serial_number)
        print(dti_info)
        print(error_code)
        print(path_road)
        print(need_add)

        infoPath = os.path.join(path_road, "info.txt")

        self.serial_number.setText(serial_number)
        self.dti_info.setText(dti_info)
        self.error_code.setText(str(error_code))
        self.path_road.setText(path_road)
        self.count.setText(str(count))
        self.listView.addItems(need_add)

        if os.path.isfile(infoPath):
            os.remove(infoPath)
        with open(infoPath, "a") as f:
            f.write(str(serial_number) + "\n")
            f.write(str(dti_info) + "\n")
            f.write(str(error_code) + "\n")
            f.write(str(need_add))
            f.close()
