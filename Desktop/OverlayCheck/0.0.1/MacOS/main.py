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
import threading
import time
import sys
import os

Resources = os.path.dirname(sys.argv[0]).replace('MacOS', 'Resources')
config_path = os.path.join(Resources, 'config.json')
for i in ['tmp', 'data', 'backup']:
    if not os.path.isdir(os.path.join(Resources, i)):
        os.makedirs(os.path.join(Resources, str(i)))


class MainFunction(QMainWindow, Ui_OverlayCheck):
    def __init__(self):
        super(MainFunction, self).__init__()
        self.setupUi(self)
        self.pushButton_4.setEnabled(False)
        self.pushButton_5.setEnabled(False)
        self.config_info = {}
        self.need_date_dict = None

    def start(self):
        self.thread = WorkerList(self.comboBox.currentText())
        self.thread.start()
        self.thread.sinOut.connect(self.run_state)

    def run_state(self, dict_info):
        self.need_date_dict = dict_info['result date']
        self.text_displat(dict_info['step'])
        if dict_info['calculate'] is True:
            threading._start_new_thread(self.display_lcd, ())
        if dict_info['result date'] is not None:
            self.table_display(dict_info['result date'])
        if dict_info['finished'] is True:
            self.show_pass_fail(dict_info['result date'])

    def table_display(self, table):
        self.tableWidget.setSortingEnabled(False)

        workbook = xlwt.Workbook()
        sheet = workbook.add_sheet("Restore Report")
        header = ['Station Name', 'Default Overlay Version', 'States', 'Issue']

        for d in range(4):
            sheet.write(0, d, header[d])

        count = 0
        for i in table:
            issue = []
            if table[i]['fail times'] > 0:
                for j in table[i]['fail report']:
                    issue.append(("[" + str(j[0]) + ' : ' + str(j[1])) + "]")
            a = [i, table[i]['default overlay'],
                 "Pass " + str(table[i]['pass times']) + ' / ' + "Fail " + str(table[i]['fail times']), issue]

            for t in range(4):
                sheet.write(count + 1, t, str(a[t]).replace('[', '').replace(']', ''))

            for j in range(4):
                new_item = QTableWidgetItem(str(a[j]).replace('[', '').replace(']', ''))
                if len(a[3]) > 0:
                    new_item.setBackground(QColor(255, 0, 0))
                mainWindow.tableWidget.setItem(count, j, new_item)
            count += 1
        workbook.save(os.path.join(Resources, 'data', time.strftime("%Y_%m_%d_%H_%M_%S") + '.xls'))
        self.tableWidget.setSortingEnabled(True)

    def show_pass_fail(self, table):
        fail = False
        for i in table:
            if len(table[i]['fail report']) > 0:
                fail = True
                break
        if fail is True:
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
            self.pushButton_4.setStyleSheet('''background-color: cyan;''')
            self.pushButton_5.setStyleSheet('''background-color: grey;''')
        else:
            self.pushButton_4.setStyleSheet('''background-color: grey;''')
            self.pushButton_5.setStyleSheet('''background-color: red;''')

    def display_lcd(self):
        time_set = int(read_json_file(config_path)['cycle_setup']['time']) - 1
        cout = 0
        while True:
            self.lcdNumber.display(str(int(time_set) - cout))
            time.sleep(1)
            cout += 1
            if cout >= time_set:
                self.lcdNumber.display("0")
                break


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
        while self.working:
            self.send_info(b='开始下载数据')
            tmp_folder = os.path.join(Resources, 'tmp')
            result = download_running(self.info, tmp_folder, self.product)

            if result is True:
                self.send_info(b="下载数据成功", a=0)

                if self.info['external command'] is True:
                    pass
                else:
                    self.send_info(b="开始处理文件", a=0)

                    state, result_date = file_process(self.info, tmp_folder, self.product)

                    if state == 0:
                        self.send_info(b="处理文件成功", a=0, d=result_date, e=True)
                    else:
                        self.send_info(b="处理文件失败", a=1, d=result_date)
            else:
                self.send_info(b="下载数据失败", a=1)

            if self.info['cycle_setup']['run'] is not True:
                break
            else:
                self.number += 1
                if self.number == self.info['cycle_setup']['times']:
                    break
                self.send_info(b='等待下次开始，等待时间 [%s]s' % str(self.info['cycle_setup']['time']), a=0, c=True)
                time.sleep(self.info['cycle_setup']['time'])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainFunction()
    mainWindow.show()
    sys.exit(app.exec())
