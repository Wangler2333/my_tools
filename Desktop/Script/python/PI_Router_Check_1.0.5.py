#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# __author__: Saseny Zhou


import sys, os
import pexpect
import psutil
import plistlib
import re
import time


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
        self.cmd = 'diskutil info OSX'
        a = self.pexpect_spaw()

        TOTAL_DISK = None
        USED_DISK_PERCENT = None
        FREE_DISK = None

        if self.ret == 0:
            for i in str(self.r).split('\\r\\n'):
                total = re.findall(r'Total Size:\s+(\d+\.?\d?) GB', i)
                free = re.findall(r'Volume Free Space:\s+(\d+\.?\d?) GB', i)

                if total:
                    TOTAL_DISK = total[0]
                if free:
                    FREE_DISK = free[0]

            if TOTAL_DISK != None and FREE_DISK != None:
                USED_DISK_PERCENT = str(
                    round(float((float(TOTAL_DISK) - float(FREE_DISK)) / float(TOTAL_DISK) * 100), 2)) + '%'

            result = TOTAL_DISK, FREE_DISK, USED_DISK_PERCENT

            return result
        else:
            return a


class remote(object):
    def __init__(self, default_file=os.path.dirname(sys.argv[0]) + '/ip_info.plist', cmd_choose=1):
        self.default = default_file
        self.check_file()
        self.cmd_choose = cmd_choose

    def check_file(self):
        if not os.path.isfile(self.default):
            info = {
                'user': 'gdlocal',
                'passwd': 'gdlocal',
                'cycle_time': '120',
                'check_file': '/Volumes/OSX/vault/data_collection/test_station_config/gh_station_info.json',
                'check_key': 'BOBCAT_DIRECT',
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
            self.file_path = a['check_file']
            self.check_key = a['check_key']
            cmd = 'cat < %s | grep %s' % (self.file_path, self.check_key)
            for i in a['ip_info'].keys():
                for j in a['ip_info'][i].keys():
                    for o in a['ip_info'][i][j].keys():
                        t = pexpect_remote(user=self.user, passwd=self.passwd, cmd='df', ip=a['ip_info'][i][j][o])
                        if self.cmd_choose == 1:
                            result = i, j, o, a['ip_info'][i][j][o], t.read_disk_df()
                            list_info.append(result)
                        elif self.cmd_choose == 2:

                            t.cmd = cmd
                            states = t.pexpect_spaw()
                            if t.ret == 0:
                                p = str(states).split(':')[1].replace('\"', '').replace(',', '').replace('\\r\\r\\n',
                                                                                                         '').replace(
                                    '\'', '')
                            else:
                                p = 'None'
                            result = i, j, o, a['ip_info'][i][j][o], t.read_disk_diskutil(), p
                            list_info.append(result)
        else:
            print('IP参数文件不正确，请检查后再试.')
            os._exit(1)

        return list_info

    def print_info(self):
        list = self.read_file()
        if self.cmd_choose == 1:
            print(
                '\n------------------' + ' 刷新时间: ' + time.strftime("%Y-%m-%d %H:%M:%S") + ' --------------------------')
            print('线别\t\t' + '\t' + '工站\t' + '\t' + 'ID\t' + '\tIP\t' + '\t' + '\t\t已用磁盘')
            for i in list:
                if '%' in str(i[4]):
                    number = str(i[4]).split('%')[0]
                    if int(number) < 30:
                        rate = '\033[0;32m' + i[4] + '\033[030m'
                    elif int(number) < 80:
                        rate = '\033[0;33m' + i[4] + '\033[030m'
                    else:
                        rate = '\033[0;31m' + i[4] + '\033[030m'

                else:
                    rate = '\033[0;31m' + i[4] + '\033[030m'

                print(i[0] + '\t\t' + i[1] + '\t\t' + i[2] + '\t\t' + i[3] + '\t\t\t' + rate)
            print('--------------------------------------------------------------------------\n')
        if self.cmd_choose == 2:
            print(
                '\n------------------' + ' 刷新时间: ' + time.strftime("%Y-%m-%d %H:%M:%S") + ' --------------------------')
            print('线别\t\t' + '\t' + '工站\t' + '\t' + 'ID\t' + '\tIP\t' + '\t\t' + self.check_key + '\t\t已用磁盘')
            for i in list:
                if '%' in str(i[4][2]):
                    number = str(i[4][2]).split('.')[0]
                    if int(number) < 30:
                        d = '\033[0;32m' + str(i[4][2]) + '\033[030m'
                    elif int(number) < 80:
                        d = '\033[0;33m' + str(i[4][2]) + '\033[030m'
                    else:
                        d = '\033[0;31m' + str(i[4][2]) + '\033[030m'
                    rate = "Total: " + str(i[4][0]) + "GB\t" + "Free: " + str(i[4][1]) + "GB\t" + "使用率: " + d
                else:
                    rate = '\033[0;31m' + str(i[4]) + '\033[030m'
                print(i[0] + '\t\t' + i[1] + '\t\t' + i[2] + '\t\t' + i[3] + '\t\t' + '\033[0;34m' + i[
                    5] + '\033[030m' + '\t\t\t' + rate)
            print('--------------------------------------------------------------------------\n')

    def read_plist(self):
        return plistlib.readPlist(self.default)


if __name__ == '__main__':
    d = remote()

    if len(sys.argv) > 1:
        if sys.argv[1] in ['-h', '-H', '-help', '--']:
            print('检测\'ip_info.plist\'所述的所有IP站点server磁盘使用状态，默认120s循环一次.')
            print('默认使用查询剩余空间命令为：[df]，当参数输入: choose2 时则选择查询命令: [diskutil info **]')
            print('1.0.4: 新增检测循环时间设置. \'ip_info.plist\'文件中.')
            print('1.0.5: 新增\'BOBCAT_DIRECT\'检测设置，可设置其他检测. \'ip_info.plist\'文件中.')
            print('Version: 1.0.5 测试版')
            os._exit(1)
        elif sys.argv[1] == 'choose2':
            d.cmd_choose = 2
        else:
            os._exit(1)
    while True:
        d.print_info()
        time.sleep(int(d.read_plist()['cycle_time']))
