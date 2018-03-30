#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time     : 2018/2/8下午1:16
# @Author   : Saseny Zhou
# @Site     : 
# @File     : main.py
# @Software : PyCharm


from UI.ui_main import *
from MacOS.home import *
from MacOS.running import *
from MacOS.change import *
from config.config import *


class AuditTools(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(AuditTools, self).__init__()
        self.setupUi(self)
        self.choose = []
        self.ui_config = self.read_config()
        self.main_window()

    def read_config(self):
        reader = read_json_file(os.path.join(resources, "config.json"))
        if reader is False:
            writer_config()
            self.read_config()
        return reader

    def home(self):
        self.home = HomeSet()
        self.home.show()

    def running(self):
        if len(self.choose) > 0:
            self.running = RunningShow(self.choose)
            self.running.show()
            self.hide()
            self.running.close_signal.connect(self.show)

    def open(self):
        os.system("open ~/Downloads")

    def main_window(self):
        products = self.ui_config["product-station-command"].keys()
        self.listWidget.addItems(products)
        self.listWidget.doubleClicked.connect(self.second_window)

    def second_window(self, info):
        data = info.data()
        self.listWidget_2.clear()
        self.listWidget_2.addItems(self.ui_config["product-station-command"][data].keys())
        self.listWidget_2.doubleClicked.connect(self.third_window)

    def third_window(self, info):
        product = list(self.ui_config["product-station-command"].keys())[self.listWidget.currentRow()]
        data = info.data()
        tmp = str(product) + interval + str(data)
        if tmp not in self.choose:
            self.choose.append(tmp)
        self.listWidget_3.clear()
        self.listWidget_3.addItems(self.choose)
        self.listWidget_3.doubleClicked.connect(self.item_setUp)

    def item_setUp(self, info):
        self.change_set = ChangeSet(info.data())
        self.change_set.setWindowTitle(info.data())
        self.change_set.show()
        self.change_set.delete_signal.connect(self.set_up_item)

    def set_up_item(self, dict_):
        product = str(dict_["product"]).split(interval)[0]
        station = str(dict_["product"]).split(interval)[1]

        tmp_dict = self.ui_config["product-station-command"][product][station]

        source_command_path = os.path.join(command_define_path, tmp_dict["cmd-link"])
        source_config_path = os.path.join(command_define_path, tmp_dict["config"])

        create_folder(os.path.dirname(source_command_path))
        create_folder(os.path.dirname(source_config_path))

        if dict_["delete"] is True:
            self.choose.remove(dict_["product"])
            self.listWidget_3.clear()
            self.listWidget_3.addItems(self.choose)

        if dict_["command"] is True:
            cmd_name, _ = QFileDialog.getOpenFileName(self, "Choose Command", "/", "file (*.command *.sh *.py)")
            if cmd_name:
                os.system("cp -rf %s %s" % (cmd_name, source_command_path))
                self.change_set.close()

        if dict_["config"] is True:
            config_name, _ = QFileDialog.getOpenFileName(self, "Choose Config", "/", "file (*.json)")
            if config_name:
                os.system("cp -rf %s %s" % (config_name, source_config_path))
                self.change_set.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = AuditTools()
    mainWindow.show()
    sys.exit(app.exec())
