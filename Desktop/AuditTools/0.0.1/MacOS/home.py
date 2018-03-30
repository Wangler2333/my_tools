#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time     : 2018/2/8下午1:16
# @Author   : Saseny Zhou
# @Site     : 
# @File     : home.py
# @Software : PyCharm


from UI.ui_home import *
from PyQt5.QtWidgets import *
from functions.json_file import *


class HomeSet(QMainWindow, Ui_home):
    def __init__(self):
        super(HomeSet, self).__init__()
        self.setupUi(self)
        self.show_update_time()

    def write_tokenID(self):
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        tokenID = self.lineEdit.text()
        if re.findall(r'^[A-z0-9]+$', str(tokenID)):
            self.lineEdit.setText("Update succeed, update time: %s" % str(current_time))
            obj = {
                "tokenID": tokenID,
                "Update": current_time
            }
            write_json_file(obj, os.path.join(resources, "token.json"))
        else:
            self.lineEdit.setText("Pls re-input tokenID")
        print(current_time)

    def show_update_time(self):
        obj = read_json_file(os.path.join(resources, "token.json"))
        if obj is not False:
            self.lineEdit.setText("Update Time: %s" % str(obj["Update"]))

    def load_config(self):
        config_name, _ = QFileDialog.getOpenFileName(self, "Load New Config", "/", "file (*.json)")
        if config_name:
            os.system("cp -rf %s %s" % (config_name, os.path.join(resources, "config.json")))
            self.label.setText("Load new main config succeed!")
