#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __author__: Saseny Zhou
# Created on 2017/09/08


from ui_mytools import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from graphPic import *
import sys, os
import plistlib
import re
import time
import threading
import _thread
import sqlite3
import shutil

datePath = os.path.dirname(sys.argv[0]).replace('MacOS', 'Resources')
usedPath = os.path.expanduser('~')


class my_tools(QMainWindow, Ui_MyTools):
    def __init__(self):
        super(my_tools, self).__init__()
        self.setupUi(self)
        self.label_3.setPixmap(QPixmap(datePath + '/2.png'))
        _thread.start_new_thread(self.timedisplay, ())

    def timedisplay(self):
        while True:
            self.lcdNumber_2.display(time.strftime("%X", time.localtime()))

    def picupdate(self):
        if os.path.isfile(datePath + '/squares_plot.png'):
            os.remove(datePath + '/squares_plot.png')
        self.t = graph(savePath=datePath)
        a = self.lineEdit_6.text()

        x_label = ['PRE-SWDL','XenonBox','DP','TBT','ADA','FORCE','ACTUATOR','FACT','BUTTON','WiPAS','Coex','NAND','SW-DOWNLOAD','RUN-IN','RGBW','FLICKER','LL','FOS','GRAPE','POST-BURN','SS']
        if a == 'Yield':
            y_axle = ['99.97','99.63','99.91','99.91','99.96','99.96','99.88','98.47','99.77','98.37','99.9','99.1','99.95','98.12','99.71','99.86','98.07','99.94','99.77','98.62','100']
        if a == 'RetestRate':
            y_axle = ['0.86','5.75','2.91','2.32','0.96','0.74','1.67','5.28','1.01','2.8','0.44','1.27','3.23','6.12','3.18','0.52','3.57','2.01','2.28','8.51','1.53']

        x_axle = len(y_axle)
        self.t.open(str(a), x_axle, y_axle, x_label)  # RetestRate / Yield
        self.label_4.setPixmap(QPixmap(datePath + '/squares_plot.png'))

    def picstore(self):
        date = time.strftime("%Y_%m_%d_%H_%M_%S")
        shutil.copy(datePath + '/squares_plot.png', usedPath + '/Downloads/' + date + '.png')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = my_tools()
    mainWindow.show()
    sys.exit(app.exec())
