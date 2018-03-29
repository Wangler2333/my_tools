import pexpect
import re
import json
import sqlite3

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

    def cat_station_info(self):
        self.cmd = 'cat < %s' % (
            '/Volumes/OSX/vault/data_collection/test_station_config/gh_station_info.json')
        self.pexpect_spaw()
        if self.ret == 0:
            if "No such file or directory" not in str(self.r):
                for i in str(self.r).split('\\r\\n'):
                    print (i.replace('\\t\\t','').replace('\\r',''))




t = pexpect_remote(user='gdlocal',passwd='gdlocal',ip='172.23.171.193')
t.cat_station_info()

