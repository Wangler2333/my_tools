#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# __author__: Saseny Zhou


import sys, os
import pexpect
import psutil
import plistlib
import re
import time
import easygui

cmd = 'diskutil info OSX'


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
        pass


class remote(object):
    def __init__(self, default_file=os.path.dirname(sys.argv[0]) + '/ip_info.plist'):
        self.default = default_file
        self.check_file()

    def check_file(self):
        if not os.path.isfile(self.default):
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
                    }
            }
            print('IP 文件不存在，生成默认参数文件，请根据默认参数文件格式进行更改.')
            plistlib.writePlist(info, self.default)
            print(self.default)
            os._exit(1)

    def disk_info(self):
        '''
        :return: 返回当前磁盘使用率，磁盘总空间大小，磁盘剩余空间大小.
        '''
        try:
            self.disk = psutil.disk_usage('/')
            self.percent = str(self.disk.percent) + '%'
            self.total = str(round(float(self.disk.total) / (1024 * 1024 * 1024), 2)) + 'GB'
            self.free = str(round(float(self.disk.free) / (1024 * 1024 * 1024), 2)) + 'GB'

        except IOError as e:
            print('IOError', e)

        return self.percent, self.total, self.free

    def read_file(self):

        list_info = []

        try:
            a = plistlib.readPlist(self.default)
        except TypeError as e:
            print('TypeError', e)

        if a:
            self.user = a['user']
            self.passwd = a['passwd']
            for i in a['ip_info'].keys():
                for j in a['ip_info'][i].keys():
                    for o in a['ip_info'][i][j].keys():
                        t = pexpect_remote(user=self.user, passwd=self.passwd, cmd='df', ip=a['ip_info'][i][j][o])
                        result = i, j, o, a['ip_info'][i][j][o], t.read_disk_df()
                        list_info.append(result)
        else:
            print('IP参数文件不正确，请检查后再试.')
            os._exit(1)

        return list_info

    def print_info(self):
        list = self.read_file()
        for i in list:
            print('\n-------------')
            print('刷新时间: ' + time.strftime("%Y-%m-%d %H:%M:%S"))
            print('线别: ' + i[0])
            print('工站：' + i[1])
            print('ID：' + i[2])
            print('IP：' + i[3])
            number = str(i[4]).split('%')[0]
            if number.isalnum():
                if int(number) < 30:
                    print('\033[0;32m' + '已用磁盘: ' + i[4] + '\033[030m')
                elif int(number) < 80:
                    print('\033[0;33m' + '已用磁盘: ' + i[4] + '\033[030m')
                else:
                    print('\033[0;31m' + '已用磁盘: ' + i[4] + '\033[030m')
                    time.sleep(600)
                    self.show_prompt(time.strftime("%Y-%m-%d %H:%M:%S"), i[0], i[1], i[2], i[3], i[4])
                print('-------------\n')
            else:
                print('\033[0;31m' + '已用磁盘: ' + i[4] + '\033[030m')
                self.show_prompt(time.strftime("%Y-%m-%d %H:%M:%S"), i[0], i[1], i[2], i[3], i[4])

    def show_prompt(self, a, b, c, d, e, f):
        time = '刷新时间: ' + a
        line = '线别: ' + b
        station = '工站：' + c
        station_id = 'ID：' + d
        ip_address = 'IP：' + e
        disk_state = '已用磁盘: ' + f
        result = time + '\n' + line + '\n' + station + '\n' + station_id + '\n' + ip_address + '\n' + disk_state
        easygui.msgbox(result, image=os.path.dirname(sys.argv[0]) + '/prompt.png')


if __name__ == '__main__':
    if len(sys.argv) > 1:
        print('检测\'ip_info.plist\'所述的所有IP站点server磁盘使用状态，120s循环一次.')
        print('Version: 1.0.1 测试版')
        os._exit(1)

    d = remote()
    while True:
        d.print_info()
        time.sleep(120)
