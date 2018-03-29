#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from PyQt5 import QtWidgets
import sys

app = QtWidgets.QApplication(sys.argv)

w = QtWidgets.QWidget()

w.resize(250,150)

w.move(300,300)

w.setWindowTitle('First QT5')

w.show()


sys.exit(app.exec())