#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# __author__: Saseny Zhou


import sys, os
import pexpect
import psutil
import ui_new
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import re

info = {
    'user': 'gdlocal',
    'passwd': 'gdlocal',
    'ip_info':
        {
            'F16-1FT-C16': {
                'PRE_PI': {
                    '1': '172.22.145.167'
                },
                'RUN_PI': {
                    '1': '172.22.145.167'
                },
                'POST_PI': {
                    '1': '172.22.145.167'
                },
            },
            'F16-1FT-D16': {
                'PRE_PI': {
                    '1': '172.22.145.167'
                },
                'RUN_PI': {
                    '1': '172.22.145.167'
                },
                'POST_PI': {
                    '1': '172.22.145.167'
                }
            },
            'F16-2FT-F16': {
                'PRE_PI': {
                    '1': '172.22.145.167'
                },
                'RUN_PI': {
                    '1': '172.22.145.167'
                },
                'POST_PI': {
                    '1': '172.22.145.167'
                }
            },
            'F16-2FT-G16': {
                'PRE_PI': {
                    '1': '172.22.145.167'
                },
                'RUN_PI': {
                    '1': '172.22.145.167'
                },
                'POST_PI': {
                    '1': '172.22.145.167'
                }
            }
        }
}


# print (type(info))

# plistlib.writePlist(info, os.path.dirname(sys.argv[0]) + '/ip_info.plist')


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
            ssh.sendline()
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

    def another(self):
        child = pexpect.spawn('ssh %s@%s' % (self.user, self.ip),  timeout=3)
        child.expect('Password:')
        child.sendline(self.passwd)
        child.expect(r'Bundle:~ bundle$')
        child.sendline(self.cmd)
        print (child.read())

'''
ccm = 'screencapture -o /Users/jamin/Desktop/new_check.png'
t = pexpect_remote(user='bundle', passwd='bundle', ip='172.22.145.165', cmd=ccm)
#print(t.pexpect_spaw())
t.cmd = 'df'
print(t.pexpect_spaw())
t.another()
'''

class Find(QDialog,ui_new.Ui_MainWindow):
    def __init__(self,text,parent=None):
        super(Find,self).__init__(parent)
        self.__text = text
        self.__index = 0
        self.setupUi(self)
        self.setupUi(self)



t = Find