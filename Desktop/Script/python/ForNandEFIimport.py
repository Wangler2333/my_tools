#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import pexpect
import sys
import os

'''
程序目标功能:
     1. 文件复制
          a. 复制文件到第一层IP(nand)
          b. 通过一层IP再次复制到二层IP并放入目标文件夹
          c. 对放入文件进行权限授予
     2. 文件检查
          a. 进入一层IP，再次进入二层IP
          b. 进行远程控制，命令输入，对dmg文档进行解压检测
'''


# 1. 文件复制
def copy_file(ip,sourcefile):
    for i in range(5):
        ssh = pexpect.spawn('scp %s gdlocal@%s:/Users/gdlocal/Desktop' % sourcefile)
        i = ssh.expect(['Are you sure you want to continue connecting (yes/no)?', '*assword:'])
        if i == 0:
            ssh.sendline('yes')
            ssh.expect('*assword:')
            ssh.sendline('gdlocal')
        elif i == 1:
            ssh.sendline('gdlocal')

        if "100%" in ssh.read():
            break

    for i in range(10):
        if i == 9:
            print "-> 连接失败,请检查网络连接."
            os._exit(1)
        try:
            child = pexpect.spawn('ssh gdlocal@%s' % ip)
            status = child.expect(['Are you sure you want to continue connecting (yes/no)?', '*assword:'])
            if status == 0:
                child.sendline('yes')
                child.expect('*assword:')
                child.sendline('gdlocal')
                break
            elif status == 1:
                child.sendline('gdlocal')
                break
        except:
            continue

    sourcefile_two = os.path.basename(sourcefile)
    cmd = 'scp %s gdadmin@10.0.100.2:/' % ('/Users/gdlocal/Desktop' + sourcefile_two)

    for i in range(5):
        if i == 4:
            print "-> 连接失败,请检查网络连接."
            os._exit(1)
        try:
            child.expect('*gdlocal*')
            child.sendline(cmd)
            status = child.expect(['Are you sure you want to continue connecting (yes/no)?', '*assword:'])
            if status == 0:
                child.sendline('yes')
                child.expect('*assword:')
                child.sendline('gdadmin')
            elif status == 1:
                child.sendline('gdadmin')

            # 授权命令

        except pexpect.EOF, pexpect.TIMEOUT:
            print ip + sys.argv[1] + " timeout"


def check_dmg(ip):
    for i in range(9):
        if i == 9:
            print "-> 连接失败,请检查网络连接."
            os._exit(1)
        try:
            child = pexpect.spawn('ssh gdlocal@%s' % ip)
            status = child.expect(['Are you sure you want to continue connecting (yes/no)?', '*assword:'])
            if status == 0:
                child.sendline('yes')
                child.expect('*assword:')
                child.sendline('gdlocal')
                break
            elif status == 1:
                child.sendline('gdlocal')
                break
        except:
            continue

        cmd = 'ssh gdadmin@10.0.100.2'
        child.sendline(cmd)
        status = child.expect(['Are you sure you want to continue connecting (yes/no)?', '*assword:'])
        if status == 0:
            child.sendline('yes')
            child.expect('*assword:')
            child.sendline('gdadmin')

        elif status == 1:
            child.sendline('gdadmin')

        cmd2 = "解压dmg"
        cmd3 = "检测dmg文档内"
        child.sendline(cmd2)
        child.sendline(cmd3)
        print child.read()

