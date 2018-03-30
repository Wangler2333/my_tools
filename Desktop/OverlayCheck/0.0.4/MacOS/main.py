#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time     : 2017/12/9上午8:36
# @Author   : Saseny Zhou
# @Site     : 
# @File     : main.py
# @Software : PyCharm Community Edition

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from UI.overlay_check import *
from Config.config import *
from Functions.excel_process import *
from Functions.shell import *
from Change_History.history import *
from Functions.crawl import *
import threading
import time
import sys
import os

Resources = os.path.dirname(sys.argv[0]).replace('MacOS', 'Resources')
config_path = os.path.join(Resources, 'config.json')
for i in ['tmp', 'data', 'backup']:
    if not os.path.isdir(os.path.join(Resources, i)):
        os.makedirs(os.path.join(Resources, str(i)))
config_check(config_path)
write_history(os.path.join(Resources, 'history.txt'), history)


class MainFunction(QMainWindow, Ui_OverlayCheck):
    def __init__(self):
        super(MainFunction, self).__init__()
        self.setupUi(self)
        self.pushButton_5.setEnabled(False)
        self.config_info = {}
        self.need_date_dict = None
        if self.checkBox.isChecked() is True:
            self.default_config()

    def start(self):
        self.thread = WorkerList(self.comboBox.currentText())
        self.thread.start()
        self.thread.sinOut.connect(self.run_state)
        self.pushButton_2.setEnabled(False)

    def run_state(self, dict_info):
        self.need_date_dict = dict_info['result date']
        self.text_displat(dict_info['step'])
        if dict_info['calculate'] is True:
            threading._start_new_thread(self.display_lcd, ())
        if dict_info['result date'] is not None:
            self.table_display(dict_info['result date'])

    def table_display(self, table):
        fail_now = False
        self.tableWidget.clearContents()
        self.tableWidget.setSortingEnabled(False)
        count = 0
        for i in table:
            for j in range(4):
                new_item = QTableWidgetItem(str(i[j]).replace('[', '').replace(']', ''))
                if int(str(i[2]).split('F /')[0]) > 0 and j == 2:
                    fail_now = True
                    new_item.setBackground(QColor(255, 0, 0))
                mainWindow.tableWidget.setItem(count, j, new_item)
            count += 1
        self.show_pass_fail(fail_now)
        self.tableWidget.setSortingEnabled(True)

    def show_pass_fail(self, fails):
        if fails is True:
            self.state_display(1)
        else:
            self.state_display(0)

    def export_data(self):
        os.system('open %s' % os.path.join(Resources, 'data'))

    def default_config(self):
        if self.checkBox.isChecked() is True:
            self.config_info = read_json_file(config_path)
            self.comboBox.clear()
            self.comboBox.addItems(self.config_info['product_info'].keys())

    def load_new_config(self):
        a, b = QtWidgets.QFileDialog.getOpenFileName(self, 'Choose config File for load', '/', "(*.json)")
        if a:
            c = read_json_file(a)
            if c is not False:
                if write_json_file(c, config_path) is not False:
                    self.text_displat("新配置文件加载成功.")
                    self.default_config()

    def text_displat(self, message):
        current_time = time.strftime("%Y/%m/%d %H:%M:%S")
        self.textEdit.append(str(current_time) + " --> " + str(message))

    def state_display(self, state):
        if state == 0:
            self.pushButton_5.setStyleSheet('''background-color: cyan;''')
            self.pushButton_5.setText('PASS')
        else:
            self.pushButton_5.setStyleSheet('''background-color: red;''')
            self.pushButton_5.setText('FAIL')

    def display_lcd(self):
        time_set = int(read_json_file(config_path)['cycle_setup']['time'])
        while time_set:
            time_string = seconds_to_time(time_set)
            self.lcdNumber.display(str(time_string))
            time_set -= 1
            time.sleep(1)
        self.lcdNumber.display(str("00:00:00"))


class WorkerList(QThread):
    sinOut = pyqtSignal(dict)

    def __init__(self, dict_info=None, parent=None):
        super(WorkerList, self).__init__(parent)
        self.product = dict_info
        self.info = read_json_file(config_path)
        self.working = True
        self.resend_dict = {}
        self.number = 0

    def __del__(self):
        self.working = False
        # self.wait()

    def send_info(self, a=0, b='', c=False, d=None, e=False):
        self.resend_dict = {
            'result code': a,
            'step': b,
            'calculate': c,
            'result date': d,
            'finished': e
        }
        self.sinOut.emit(self.resend_dict)

    def run(self):
        retry_times = 0
        while self.working:
            self.send_info(b='开始下载数据')
            tmp_folder = os.path.join(Resources, 'tmp')

            # result = download_running(self.info, tmp_folder, self.product)
            result = crawl(tmp_folder)

            if result is True:
                self.send_info(b="下载数据成功", a=0)

                print(self.info)
                if self.info['external command']['run'] is True:
                    pass
                else:
                    self.send_info(b="开始处理文件", a=0)

                    state, result_date = file_process(self.info, tmp_folder, self.product)

                    if state == 0:
                        self.send_info(b="处理文件成功", a=0, d=result_date, e=True)
                    else:
                        self.send_info(b="处理文件失败", a=1, d=result_date)
                        if retry_times < self.info["retry times"]:
                            self.send_info(
                                b="第[%s]次 retry, 5s后开始 retry, retry 次数设定[%s]" % (
                                    str(retry_times + 1), str(self.info["retry times"])), a=1)
                            time.sleep(5)
                            retry_times += 1
                            continue
            else:
                self.send_info(b="下载数据失败", a=1)
                if retry_times < self.info["retry times"]:
                    self.send_info(
                        b="第[%s]次 retry, 5s后开始 retry, retry 次数设定[%s]" % (
                            str(retry_times + 1), str(self.info["retry times"])), a=1)
                    time.sleep(5)
                    retry_times += 1
                    continue

            if self.info['cycle_setup']['run'] is not True:
                break
            else:
                self.number += 1
                if self.number == self.info['cycle_setup']['times']:
                    break
                self.send_info(b='等待下次开始，等待时间 [%s]s' % str(self.info['cycle_setup']['time']), a=0, c=True)
                time.sleep(self.info['cycle_setup']['time'])
            retry_times = 0


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainFunction()
    mainWindow.show()
    sys.exit(app.exec())
