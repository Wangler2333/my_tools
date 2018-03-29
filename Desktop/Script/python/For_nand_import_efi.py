#!/usr/bin/env python
# -*- coding: UTF-8 -*-


import pexpect
import commands

passwd_remote = "gdlocal"
passed_mini = "gdadmin"
copy_cmd = ""

miniIP = "10.0.100.2"


def ssh_cmd(user, ip,passwd, cmd):
    ret = -1
    ssh = pexpect.spawn('ssh %s@%s %s' % (user, ip, cmd))
    try:
        i = ssh.expect(['Password:', 'Are you sure you want to continue connectinng (yes/no)?'], timeout=2)
        if i == 0:
            ssh.sendline(passwd)

        elif i == 1:
            ssh.sendline('yes/n')
            ssh.expect('Password:')
            ssh.sendline(passwd)

        ssh.sendline(cmd)

        j = ssh.expect(['Password:',''], timeout=2)
        if j == 0:
            ssh.sendline('gdadmin')
        elif j == 1:
            pass
        r = ssh.read()
        print r

        #'''
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

def copy_log_to_remote(soucrepath,user,ip,tagetpath,passwd):
    foo = pexpect.spawn('scp -r %s %s@%s:%s'% (soucrepath,user,ip,tagetpath))
    i = foo.expect(['Password:', 'Are you sure you want to continue connectinng (yes/no)?'], timeout=2)
    if i == 0:
        foo.sendline(passwd)
    elif i == 1:
        foo.sendline('yes/n')
        foo.expect('Password:')
        foo.sendline(passwd)
    print foo.read()



#cmd = "scp -r /Users/gdlocal/Desktop/SigningBypass.psplist...zip gdadmin@10.0.100.2:/Library/NetBoot/NetBootSP0/TAEFI.nbi"
#cmd = 'date'
copy_log_to_remote('/Users/saseny/Desktop/SigningBypass.psplist...zip','gdlocal','172.23.164.107','/Users/gdlocal/Desktop','gdlocal')
#cmd = copy_log_to_remote('/Users/gdlocal/Desktop/SigningBypass.psplist...zip','gdadmin','10.0.100.2','/Library/NetBoot/NetBootSP0/TAEFI.nbi','gdadmin')

cmd = 'sudo -s'
ssh_cmd('bundle','172.22.145.90','bundle',cmd)