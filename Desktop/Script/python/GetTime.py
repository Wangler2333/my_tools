#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import pexpect
import re

'''
user:           远程服务器账户
ip:             远程服务器IP
cmd:            命令行用于得到服务器当前时间
passwd_remote:  远程服务器登录密码
passwd_local:   本地开机密码
'''

user = "saseny"
ip = "172.22.145.137"
cmd = "date +%m/%d/%Y_%H:%M:%S"
passwd_remote = "SasenyZhou"
passwd_local = "bundle"


def Set_Time(set_cmd):
    '''
    :param set_cmd: 给定命令行，然后run，给的命令一般都要是需要在root权限下才能跑得，
                    不然用这格式就没什么意义了,直接可以用os.system或者commands.getoutput就可以了
    :return: 没有返回值
    '''
    foo = pexpect.spawn('%s' % set_cmd)
    foo.expect('.assword:*')
    foo.sendline(passwd_local)
    foo.interact()


def set_local_time(times):
    '''
    :param times: 输入参数是得到的时间，(日期加时间)
    :return:
    '''
    try:
        get_date = re.findall(r'[0-9]{2}/[0-9]{2}/[0-9]{4}', str(times))[0].replace('/', ':')
        get_time = re.findall(r'[0-9]{2}:[0-9]{2}:[0-9]{2}', str(times))[0]

        turn_off_auto_time = 'sudo systemsetup -setusingnetworktime off'
        turn_on_auto_time = 'sudo systemsetup -setusingnetworktime on'
        set_date_cmd = 'sudo systemsetup -setdate %s' % get_date
        set_time_cmd = 'sudo systemsetup -settime %s' % get_time

        if passwd_local != passwd_remote:
            Set_Time(turn_off_auto_time)
            Set_Time(set_date_cmd)
            Set_Time(set_time_cmd)
            Set_Time(turn_on_auto_time)

    except:
        pass


def ssh_cmd():
    '''
    :return: 连接远程服务器，得到远程服务器的时间并赋予函数set_local_time，进行处理
    '''
    ret = -1
    ssh = pexpect.spawn('ssh %s@%s "%s"' % (user, ip, cmd))
    try:
        i = ssh.expect(['Password:', 'connectinng (yes/no)?'], timeout=2)
        if i == 0:
            ssh.sendline(passwd_remote)
        elif i == 1:
            ssh.sendline('yes/n')
            ssh.expect('Password:')
            ssh.sendline(passwd_remote)
        ssh.sendline(cmd)
        r = ssh.read()
        set_local_time(r)
        # print r
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


if __name__ == '__main__':
    ssh_cmd()
