#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time     : 2018/3/8下午3:04
# @Author   : Saseny Zhou
# @Site     : 
# @File     : home.py
# @Software : PyCharm


from UI.ui_home import *
from PyQt5.QtWidgets import *


class HomeSet(QMainWindow, Ui_Home):
    def __init__(self):
        super(HomeSet, self).__init__()
        self.setupUi(self)
        self.center()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def loadConfig(self):
        config_name, _ = QFileDialog.getOpenFileName(self, "Load New Config", "/", "file (*.json)")
        if config_name:
            os.system("cp -rf %s %s" % (config_name, os.path.join(resources, "config.json")))
            self.label.setText("Load new main config succeed!")
            collectLogs.logger.debug("Load New Config Passed. Info: {}".format(config_name))

    def changeToken(self):
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        tokenID = self.tokenID.text()
        if re.findall(r'^[A-z0-9]+$', str(tokenID)):
            self.tokenID.setText("Update succeed, update time: %s" % str(current_time))
            obj = {
                "tokenID": tokenID,
                "Update": current_time
            }
            write_json_file(obj, os.path.join(resources, "token.json"))
            collectLogs.logger.debug("Write New Token Time: {}".format(current_time))
            collectLogs.logger.debug("Write New Token Passed. Info: {}".format(tokenID))
        else:
            collectLogs.logger.debug("Write New Token Failed. Info: {}".format(tokenID))
            self.tokenID.setText("Pls re-input tokenID")
