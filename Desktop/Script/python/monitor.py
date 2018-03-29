# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys, os
from ui_monitor import *
import pexpect
import plistlib
import re
import time
import threading
import _thread


class myapp_first(QMainWindow, Ui_monitorTools):
    def __init__(self):
        super(myapp_first, self).__init__()
        self.setupUi(self)
        self.label.setText('1.0.1')
        _thread.start_new_thread(self.timedisplay, ())

    def startButton(self):
        # self.updateLogs('123')
        self.showStatuBar('开始....')

        _thread.start_new_thread(cycleRun, ())
        _thread.start_new(updateinfo, ())

    def onceUpdate(self):
        _thread.start_new_thread(main_run, ())

    def clearButton(self):
        self.clearup()

    def clearLogsButton(self):
        self.clearLogs()

    def addIp(self):
        filepath = os.path.dirname(sys.argv[0]) + '/ip.txt'
        a = self.lineEdit.text()

        writed = True

        if re.findall(r'\d+\.\d+\.\d+\.\d+', a) and os.path.isfile(filepath):
            dd = open(filepath, 'r')
            for e in dd.readlines():
                if a in e.replace('\n', ''):
                    print(a)
                    print(e.replace('\n', ''))
                    writed = False
            dd.close()

            if writed == True:
                f = open(filepath, 'a')
                f.write(str(a) + '\n')
                f.close()
            else:
                self.label_2.setText("IP已经存在")
        else:
            self.label_2.setText("请输入正确IP")

    def j79update(self, list):
        for i in range(len(list)):
            for j in range(9):
                # self.tableWidget.setItem(i, j, QTableWidgetItem(list[i][j]))
                _thread.start_new_thread(setvalue, (i, j, list))

    def j80update(self, list):
        for i in range(len(list)):
            for j in range(9):
                # self.tableWidget_2.setItem(i, j, QTableWidgetItem(list[i][j]))
                _thread.start_new_thread(setvalue2, (i, j, list))

    def showStatuBar(self, content):
        self.statusBar.setStatusTip('正在抓取IP: ' + str(content) + ' 的信息........')

    def updateLogs(self, content):
        currentTime = time.strftime("%Y-%m-%d %H:%M:%S")
        self.textEdit.append(currentTime + ': ' + str(content) + '\n')

    def clearLogs(self):
        self.textEdit.clear()

    def timedisplay(self):
        while True:
            self.lcdNumber.display(time.strftime("%X", time.localtime()))

    def clearup(self):
        for j in range(30):
            for i in range(9):
                self.tableWidget.setItem(j, i, QTableWidgetItem(""))
                self.tableWidget_2.setItem(j, i, QTableWidgetItem(""))


def updateinfo():
    while True:
        info_79 = []
        info_80 = []
        None_list = []
        list = read_info_file()

        # print (list)

        for i in list:
            if "79" in i[-1]:
                info_79.append(i)
            elif "80" in i[-1]:
                info_80.append(i)
            else:
                None_list.append(i)

        # print(info_79)
        # print(info_80)
        # print(None_list)

        mainWindow.j79update(info_79)
        mainWindow.j80update(info_80)
        for pp in None_list:
            mainWindow.updateLogs(pp[3] + "  --> Remote Fail, Pls Check.")

        time.sleep(10)


def setvalue(i, j, list):
    mainWindow.tableWidget.setItem(i, j, QTableWidgetItem(list[i][j]))


def setvalue2(i, j, list):
    mainWindow.tableWidget_2.setItem(i, j, QTableWidgetItem(list[i][j]))


class pexpect_remote(object):
    def __init__(self, user=None, ip=None, passwd=None, cmd=None):
        self.user = user
        self.ip = ip
        self.passwd = passwd
        self.cmd = cmd

    def pexpect_spaw(self):
        self.ret = -1
        ssh = pexpect.spawn('ssh %s@%s %s' % (self.user, self.ip, self.cmd))
        try:
            i = ssh.expect(['Password:', 'Are you sure you want to continue connecting (yes/no)?'], timeout=2)
            if i == 0:
                ssh.sendline(self.passwd)

            elif i == 1:
                ssh.sendline('yes/n')
                ssh.expect('Password:')
                ssh.sendline(self.passwd)
            self.r = ssh.read()
            ssh.close()
            self.ret = 0
        except pexpect.EOF:
            msg = 'EOF'
            ssh.close()
            self.ret = -1

        except pexpect.TIMEOUT:
            msg = 'TIMEOUT'
            ssh.close()
            self.ret = -2

        if self.ret == 0:
            return self.r
        else:
            return 'Error: ' + msg

    def read_disk_df(self):
        a = self.pexpect_spaw()
        capacity = []
        if self.ret == 0:
            for i in str(self.r).split('\\r\\n'):
                if '/' in i:
                    tb = re.compile(r'(\d+%)')
                    f = tb.findall(i)
                    capacity.append(f)
            return capacity[0][0]
        else:
            return a

    def read_disk_diskutil(self):
        self.cmd = "diskutil info OSX"
        self.pexpect_spaw()

        if self.ret == 0:
            total = 0
            free = 0
            for i in str(self.r).split('\\r\\n'):
                if "Total Size:" in i:
                    total = i.split()[2]
                if "Volume Free Space:" in i:
                    free = i.split()[3]
            rate = str(round(((float(total) - float(free)) / float(total)) * 100, 2)) + '%'
            # result = str(free) + 'GB Used:' + rate
            return rate

        else:
            return "None"

    def read_bobcat_state(self):
        self.cmd = 'cat < %s | grep %s' % (
            '/Volumes/OSX/vault/data_collection/test_station_config/gh_station_info.json', 'BOBCAT_DIRECT')
        states = self.pexpect_spaw()
        if self.ret == 0:
            td = str(states).replace('BOBCAT_DIRECT', '').replace('\\n', '').replace('\\t',
                                                                                     '').replace(
                '\\r', '')
            d = re.findall(r'\w+', td)
            if len(d) > 0:
                result = d[-1]
            else:
                result = 'None'
        else:
            result = 'None'

        return result

    def read_pi_router_info(self):
        self.cmd = 'cat < %s' % '/Users/gdlocal/Desktop/Restore*.txt'
        file = self.pexpect_spaw()
        PRODUCT = "None"
        LINE = "None"
        STATION = "None"
        ID = "None"
        OVERLAY = "None"
        if self.ret == 0:

            if "No such file or directory" not in str(self.r):
                for i in str(self.r).split('\\r\\n'):
                    # print(i)
                    if "PRODUCT=" in i:
                        PRODUCT = i.split('PRODUCT=')[1]
                    if "LINE=" in i:
                        LINE = i.split('LINE=')[1]
                    if "UNIT=" in i:
                        a = i.split('UNIT=')[1].split()
                        if len(a) == 3:
                            STATION = a[1]
                            ID = a[2]
                    if "STATION_OVERLAY_VERSION=" in i:
                        OVERLAY = i.split('STATION_OVERLAY_VERSION=')[1].split()[1].split('_')[-1]
                return (PRODUCT, LINE, STATION, ID, OVERLAY)

            else:
                return "None"
        else:
            return "None"


def main_run():
    file = os.path.dirname(sys.argv[0]) + '/ip.txt'
    file_path = '/Users/Shared/monitor/info/'
    os.system('mkdir -p %s' % file_path)

    if os.path.isfile(file):
        f = open(file, 'r')
        for i in f.readlines():
            t = pexpect_remote(user='gdlocal', passwd='gdlocal')
            ip = i.replace('\n', '')
            t.ip = ip
            if "None" in t.read_disk_diskutil():
                used = ""
            else:
                used = t.read_disk_diskutil()
            if "None" in t.read_bobcat_state():
                state = "None"
            else:
                state = t.read_bobcat_state()

            if "None" in t.read_pi_router_info():
                product = "None"
                line = "None"
                station = "None"
                id = "None"
                overlay = "None"
            else:
                product = t.read_pi_router_info()[0]
                line = t.read_pi_router_info()[1]
                station = t.read_pi_router_info()[2]
                id = t.read_pi_router_info()[3]
                overlay = t.read_pi_router_info()[4]

            result = "used:" + str(used) + '\n' + "stste:" + str(state) + '\n' + "product:" + str(
                product) + '\n' + "line:" \
                     + str(line) + '\n' + "station:" + str(station) + '\n' + "id:" + str(id) + '\n' + "overlay:" + \
                     str(overlay) + '\n' + "ip:" + str(ip) + '\n' + "time:" + str(time.strftime("%Y-%m-%d %H:%M:%S"))

            # print(result)

            p = open(file_path + product + '_' + ip + '.txt', 'w')
            p.write(str(result))
            p.close()
        f.close()


def find_file():
    try:
        a = []
        fns = [os.path.join(root, fn) for root, dirs, files in os.walk('/Users/Shared/monitor/info') for fn in
               files]
        for f in fns:
            if os.path.isfile(f):
                if ".txt" in f:
                    a.append(f)
        return a
    except IOError as o:
        print('IOError', o)


def read_info_file():
    list = find_file()

    list_return = []

    for i in list:
        if os.path.isfile(i):
            used = "None"
            line = "None"
            station = "None"
            id = "None"
            ip = "None"
            state = "None"
            overlay = "None"
            time = "None"
            product = "None"
            f = open(i, 'r')
            for j in f.readlines():
                if "used:" in j:
                    used = j.replace('\n', '').split('used:')[1]
                if "stste:" in j:
                    state = j.replace('\n', '').split('stste:')[1]
                if "product:" in j:
                    product = j.replace('\n', '').split('product:')[1]
                if "line:" in j:
                    line = j.replace('\n', '').split('line:')[1]
                if "station:" in j:
                    station = j.replace('\n', '').split('station:')[1]
                if "id:" in j:
                    id = j.replace('\n', '').split('id:')[1]
                if "overlay:" in j:
                    overlay = j.replace('\n', '').split('overlay:')[1]
                if "ip:" in j:
                    ip = j.replace('\n', '').split('ip:')[1]
                if "time:" in j:
                    time = j.replace('\n', '').split('time:')[1]

            a = [line, station, id, ip, used, state, overlay, time, product]
            list_return.append(a)

    return list_return


def cycleRun():
    while True:
        main_run()
        time.sleep(1200)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = myapp_first()
    mainWindow.show()
    sys.exit(app.exec())
