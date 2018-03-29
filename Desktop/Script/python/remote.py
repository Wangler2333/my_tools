# -*- coding: utf-8 -*-

import pexpect
import re


class pexpect_remote(object):
    def __init__(self, user=None, ip=None, passwd=None, cmd=None, disk='OSX'):
        self.user = user
        self.ip = ip
        self.passwd = passwd
        self.cmd = cmd
        self.disk = disk

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
        self.cmd = "diskutil info %s" % self.disk
        self.pexpect_spaw()

        if self.ret == 0:
            total = 0
            free = 0
            for i in str(self.r).split('\\r\\n'):
                if "Total Size:" in i:
                    total = i.split()[2]
                if "Volume Free Space:" in i:
                    free = i.split()[3]
            rate = round(((float(total) - float(free)) / float(total)) * 100, 2)
            return str(rate) + '%', str(free) + 'GB'

        else:
            return 'None', 'None'

    def read_pi_router_info(self):
        # PRODUCT, LINE_NAME, GH_STATION_NAME, STATION_NUMBER, BOBCAT_DIRECT, STATION_OVERLAY
        self.pexpect_spaw()
        if self.ret == 0:
            if 'No such file or directory' not in str(self.r):
                for i in str(self.r).split('\\t\\t'):
                    if 'PRODUCT' in i:
                        product = str(i).split('\"')[3]
                    if 'LINE_NAME' in i:
                        line = str(i).split('\"')[3]
                    if 'GH_STATION_NAME' in i:
                        station = str(i).split('\"')[3]
                    if 'STATION_NUMBER' in i:
                        number = str(i).split('\"')[3]
                    if 'BOBCAT_DIRECT' in i:
                        bobcat = str(i).split('\"')[3]
                    if 'STATION_OVERLAY' in i:
                        overlay = str(i).split('\"')[3]
                    if 'STATION_IP' in i:
                        ip = str(i).split('\"')[3]

            return str(ip), str(product), str(line), str(station), str(number), str(bobcat), str(overlay)
        else:
            return 'None', 'None', 'None', 'None', 'None', 'None', 'None'

    def returnInfo(self):
        a, b, c, d, e, f, g = self.read_pi_router_info()
        h, i = self.read_disk_diskutil()

        return a, b, c, d, e, f, g, h, i
