#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import commands
import pexpect


'''
需要开机后自动启动:
     1. jupyter notebook                IP: 172.22.145.137:8888
     2. python manage.py runserver      IP: 172.22.145.137:8000
     3. MySQL
'''

password = "SasenyZhou"
cmd_one = 'open -a /Applications/iTerm2.app /Users/saseny/Desktop/Net_Work_Running/jupyter.sh'
cmd_two = 'open -a /Applications/iTerm2.app /Users/saseny/Desktop/Net_Work_Running/python.sh'
cmd_three = 'sudo mysql.server start'


def root_run(cmd):
    ret = -1
    ssh = pexpect.spawn('%s' % cmd)
    try:
        i = ssh.expect(['Password:', 'Are you sure you want to continue connectinng (yes/no)?'], timeout=2)
        if i == 0:
            ssh.sendline(password)
        elif i == 1:
            ssh.sendline('yes/n')
            ssh.expect('Password:')
            ssh.sendline(password)
        ssh.sendline(cmd)
        r = ssh.read()
        print r
        ret = 0
    except pexpect.EOF:
        print "EOF"
        ssh.close()
        ret = -1
    except pexpect.TIMEOUT:
        print "TIMEOUT"
        ssh.close()
        ret = -2
    return ret


def running(cmd):
    foo = pexpect.spawn('%s' % cmd)
    foo.expect('.assword:*')
    foo.sendline(password)
    foo.interact()


if __name__ == '__main__':
    root_run(cmd_three)
    os.system(cmd_one)
    os.system(cmd_two)



