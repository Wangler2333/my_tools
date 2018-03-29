import pexpect
import re
import time

'''
远程连接模块
通过IP地址，用户以及密码远程读取信息
用于读取远程电脑磁盘信息，以及 /Volumes/OSX/vault/data_collection/test_station_config/gh_station_info.json 文件
'''


class pexpect_remote(object):
    def __init__(self, user='gdlocal', ip=None, passwd='gdlocal', cmd=None):
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

    def get_station_info(self, parameter):
        PRODUCT, LINEID, STATION, GH_NAME, BOBCAT, OVERLAY = ['None', 'None', 'None', 'None', 'None', 'None']
        ID, IPADDRESS = parameter
        TIME = time.strftime("%Y-%m-%d %H:%M:%S")
        self.ip = IPADDRESS
        DISK = self.read_disk_diskutil()
        self.cmd = 'cat < %s' % ('/Volumes/OSX/vault/data_collection/test_station_config/gh_station_info.json')
        self.pexpect_spaw()
        if self.ret == 0:
            if "No such file or directory" not in str(self.r):
                for i in str(self.r).split('\\r\\n'):
                    a = i.replace('\\t\\t', '').replace('\\r', '')
                    if 'PRODUCT' in a:
                        PRODUCT = str(a).split('\"')[3]
                    if 'LINE_ID' in a:
                        LINEID = str(a).split('\"')[3]
                    if 'STATION_NUMBER' in a:
                        STATION = str(a).split('\"')[3]
                    if 'GH_STATION_NAME' in a:
                        GH_NAME = str(a).split('\"')[3]
                    if 'BOBCAT_DIRECT' in a:
                        BOBCAT = str(a).split('\"')[3]
                    if 'STATION_OVERLAY' in a:
                        OVERLAY = str(a).split('\"')[3].split('_')[-1]

        return ID, IPADDRESS, PRODUCT, LINEID, STATION, GH_NAME, BOBCAT, DISK, TIME, OVERLAY


if __name__ == '__main__':
    pass
