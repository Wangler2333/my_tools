#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# __author__: Saseny Zhou


from PyQt5.QtWidgets import QApplication, QMainWindow
import sys, os
from ui_new import *


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = QMainWindow()
    w.setWindowTitle('My Tools')

    ui = Ui_MainWindow()
    ui.setupUi(w)
    w.show()

    sys.exit(app.exec_())

