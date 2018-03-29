# -*- coding: UTF-8 -*-

# from PyQt5 import QtWidgets
# from PyQt5.QtWidgets import QFileDialog
# from ui_test import *
# from PyQt5.QtWidgets import *
# from PyQt5.QtGui import *
# from PyQt5.QtCore import *
# import sys
#
#
# class myapp_first(QMainWindow, Ui_MyApp):
#     def __init__(self):
#         super(myapp_first, self).__init__()
#         self.setupUi(self)
#
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     mainWindow = myapp_first()
#     mainWindow.show()
#     sys.exit(app.exec ())
#
#


import logging

logging.basicConfig(
    filename='test.log',
    format='%(asctime)s - %(name)s - %(levelname)s -%(module)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S %p',
    level=10
)

logging.debug('debug')
logging.info('info')
logging.warning('warning')
logging.error('error')
logging.critical('critical')

# -----------------------------------

format1 = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s -%(module)s: %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S %p', )

fh1 = logging.FileHandler('test1.log')
fh2 = logging.FileHandler('test2.log')
fh3 = logging.FileHandler('test3.log')
ch = logging.StreamHandler()

fh1.setFormatter(format1)
fh2.setFormatter(format1)
fh3.setFormatter(format1)
ch.setFormatter(format1)


logger1 = logging.getLogger('egon')
logger1.setLevel(10)
logger1.addHandler(fh1)
logger1.addHandler(fh2)
logger1.addHandler(fh3)
logger1.addHandler(ch)

logger1.debug('debug')
logger1.debug('info')
logger1.debug('error')
logger1.debug('warning')
logger1.debug('critical')
