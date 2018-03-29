import sys, os
import pexpect
import psutil
import plistlib
import re
import time
import PyQt5


'''

def print_info(list):
    print('\n------------------' + ' 刷新时间: ' + time.strftime("%Y-%m-%d %H:%M:%S") + ' --------------------------')
    print('线别\t\t\t' + '\t' + '工站\t' + '\t' + '\tID\t' + '\tIP\t' + '\t' + '\t\t\t\t已用磁盘')
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


list = [['F16-1FT-D16', 'POST-PI', '3', '172.22.145.137', '36%'],
        ['F16-1FT-D16', 'POST-PI', '3', '172.22.145.13', '36%'],
        ['F16-1FT-D16', 'POST-PI', '3', '172.22.145.13', 'Error']]
print_info(list)


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
'''


