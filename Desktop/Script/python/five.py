#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import sys, os
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import time
import _thread

if len(sys.argv) == 2:
    if sys.argv[1] in ['-h', '-H', '-help']:
        print('Usage: cmd HH:MM [optional message]')
        os._exit(1)

app = QApplication(sys.argv)


def say_message(message, times):
    for i in range(times):
        os.system('say %s' % message)
        time.sleep(2)


try:
    due1 = QTime.currentTime()
    message = "Alert!"
    if len(sys.argv) < 2:
        raise ValueError
    hours, mins = sys.argv[1].split(":")
    due2 = QTime(int(hours), int(mins))
    if not due2.isValid():
        raise ValueError
    if len(sys.argv) > 2:
        message = " ".join(sys.argv[2:])
    while True:
        due1 = QTime.currentTime()
        if due1.hour() == due2.hour() and due1.minute() == due2.minute():
            break
        time.sleep(1)
    _thread.start_new_thread(say_message, (message, 5))

except ValueError:
    message = "Usage: cmd HH:MM [optional message]"

label = QLabel("<font color=red size=72><b>" + message + "</b></font>")
# label.setWindowFlag(Qt.SplashScreen)
label.setWindowFlag(Qt.WindowStaysOnTopHint)
label.show()

QTimer.singleShot(60000, app.quit)
app.exec_()
