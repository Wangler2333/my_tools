#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time     : 2018/3/6下午6:58
# @Author   : Saseny Zhou
# @Site     : 
# @File     : main.py
# @Software : PyCharm


from UI.ui_main import *
from MacOS.login import *
from MacOS.home import *
from MacOS.payload import *
from MacOS.delete import *
from MacOS.running import *
from Config.code import *
from Config.server import *
from Config.config import *

main_config = read_json_file(os.path.join(resources, "config.json"))
collectLogs.logger.info("CONFIG INFO: \n {}".format(main_config))
if main_config is False:
    writer_config()
    main_config = read_json_file(os.path.join(resources, "config.json"))
    collectLogs.logger.info("CONFIG INFO: \n {}".format(main_config))

if not os.path.isfile(os.path.join(resources, "code.json")):
    collectLogs.logger.debug("Write Default {} File.".format(os.path.join(resources, "code.json")))
    writer_code()

if not os.path.isfile(os.path.join(resources, "service.json")):
    collectLogs.logger.debug("Write Default {} File.".format(os.path.join(resources, "service.json")))
    writer_service()


class MainWindows(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindows, self).__init__()
        self.setupUi(self)
        self.center()

        """初始化登录状态False"""
        self.loginStates = False

        """初始化选择项目为空"""
        self.chooseItems = []

        self.config = main_config["product-station-command"]
        self.firstList()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def firstList(self):
        products = self.config.keys()
        self.productList.addItems(products)
        self.productList.doubleClicked.connect(self.secondList)

    def secondList(self, info):
        data = info.data()
        collectLogs.logger.info("Choose Product: {}".format(data))
        self.stationList.clear()
        self.stationList.addItems(self.config[data].keys())
        self.stationList.doubleClicked.connect(self.payloadUI)

    def thirdList(self):
        choose = []
        for i in self.chooseItems:
            product = str(i["productCode"][0])
            station = str(i["parametricType"][0]["stationType"])
            tmp = {
                interval.join([product, station]): i
            }
            if tmp not in choose:
                choose.append(tmp)
        items = []
        for i in choose:
            for j in i.keys():
                items.append(j)
        self.chooseList.clear()
        self.chooseList.addItems(items)
        self.chooseList.doubleClicked.connect(self.itemDelete)

    def itemDelete(self, item):
        self.deleteConfirm = DeleteConfirm(item.data())
        self.deleteConfirm.confirmSignal.connect(self.deleteDo)
        self.deleteConfirm.show()

    def deleteDo(self, info):
        if info["confirm"] is True:
            collectLogs.logger.debug("CONFIRM DELETE {} From Run List".format(info["station"]))
            collectLogs.logger.debug("CURRENT CHOOSE STATION LIST AS BELOW:\n".format(self.chooseItems))
            item_product = str(info["station"]).split(interval)[0]
            item_station = str(info["station"]).split(interval)[1]
            for i in self.chooseItems:
                product = str(i["productCode"][0])
                station = str(i["parametricType"][0]["stationType"])
                if str(product) == str(item_product) and str(station) == str(item_station):
                    self.chooseItems.remove(i)
            self.thirdList()
        if info["confirm"] is False:
            collectLogs.logger.debug("CANCEL DELETE {} From Run List".format(info["station"]))

    def payloadUI(self, info):
        product = list(self.config.keys())[self.productList.currentRow()]
        station = info.data()
        collectLogs.logger.info("Choose Result: {} {}".format(product, station))
        self.payload_Info = PayLoad(self.loginStates, product, station)

        # self.payload_Info.setParent(self)
        # self.payload_Info.mouseReleaseEvent()

        self.payload_Info.show()
        self.payload_Info.confirmSignal.connect(self.chooseConfirm)

    def chooseConfirm(self, dictInfo):
        collectLogs.logger.info("Confirm One Station Info:\n{}".format(dictInfo))
        self.chooseItems.append(dictInfo)
        self.thirdList()
        self.payload_Info.close()

    def moveEvent(self, a0: QtGui.QMoveEvent):
        collectLogs.logger.debug("Main Window Moving Position: {}".format(re.findall(r"\(.*?\)", str(self.pos()))))
        try:
            self.payload_Info.close()
        except:
            pass

        try:
            self.home_Set.close()
        except:
            pass

        try:
            self.login.close()
        except:
            pass

        try:
            self.deleteConfirm.close()
        except:
            pass

    def closeEvent(self, a0: QtGui.QCloseEvent):
        collectLogs.logger.debug("Close Main Window")
        try:
            self.payload_Info.close()
        except:
            pass

        try:
            self.home_Set.close()
        except:
            pass

        try:
            self.login.close()
        except:
            pass

        try:
            self.deleteConfirm.close()
        except:
            pass

    def running(self):
        if len(self.chooseItems) > 0:
            collectLogs.logger.info("Open Running Window")
            self.runDonwload = Running(self.chooseItems)
            self.runDonwload.show()
            self.hide()
            self.runDonwload.quitSignal.connect(self.show)
        else:
            collectLogs.logger.warning("No Choose Run Items, Pls Check!")

    def homeSet(self):
        self.home_Set = HomeSet()
        self.home_Set.show()

    def openFile(self):
        os.system("open {}".format("~/Downloads"))
        collectLogs.logger.info("Open Result File: {}".format("/Downloads"))

    def loginUser(self):
        self.login = LogIn()
        self.login.show()
        self.login.login_signal.connect(self.login_Confirm)

    def login_Confirm(self):
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(imagePath + "/user_on.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionUser.setIcon(icon)
        self.loginStates = True
        collectLogs.logger.debug("LOGIN STATES: {}".format(self.loginStates))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindows()
    mainWindow.show()
    sys.exit(app.exec())
