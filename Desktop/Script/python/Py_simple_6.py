#!/usr/bin/env python
# coding: UTF-8

import glob,os,tarfile,gzip,IPy,psutil,pexpect,threading,thread,Queue,commands

Path = "/Users/saseny/Desktop/dTEST"

#file = glob.glob(Path + '/*.tgz')
#file_ = file[0].split('.tgz')[0]

#if tarfile.is_tarfile(file[0]):
#    os.system('cd %s ; tar -xzf %s &>/dev/null' %(Path,file[0]))

#    processlog = None
#    if glob.glob(file_ + '/*/*.plog'):
#        processlog = glob.glob(file_ + '/*/*.plog')
#    if glob.glob(file_ + '/*/*/*.plog'):
#        processlog = glob.glob(file_ + '/*/*/*.plog')
#    if processlog:
#        processlog = processlog[0]
#print processlog


def ExpectCMD(cmd, passwd):
	ssh = pexpect.spawn('sudo %s' % (cmd))
	print 'sudo %s' % (cmd)
	try:
		i = ssh.expect(['yes/no', 'assword:', '\*',pexpect.EOF], timeout=240)
		if i == 1 :
			ssh.sendline(passwd)
			print 'passwd *********'
		elif i == 0:
			ssh.sendline('yes\r')
			print 'yes'
			ssh.expect('assword:')
			ssh.sendline(passwd)
			print 'passwd *********'
		elif i==2:
			print 'unknow'
			print ssh.expect('assword:')
			ssh.sendline(passwd)
			print 'passwd *********'
	except pexpect.EOF:
		print "EOF"
		ssh.close()
		exit(-1)
	except pexpect.TIMEOUT:
		print "SSH TIMEOUT"
		ssh.close()
		exit(-2)


cdd = 'diskutil partitionDisk /dev/disk1 1 GPTFormat HFS+ Diagnostics 1G'
cdd1 = 'expect -c "set timeout 1;spawn sudo /usr/sbin/asr -partition /dev/disk1 -testsize 70g -retestsize 1g -recoverysize 80g; expect -re \".*password*\";send \"~Saseny\r\";expect -re \"$\";interact"'
cdd2 = 'diskutil unmountDisk /dev/disk1s3'
cdd3 = 'sudo /usr/sbin/asr -s /Users/saseny/Desktop/Log_For_Regression/Bundle/J79A_RIR_3-8_5.0B2.dmg -t /dev/disk1s3 -erase -noprompt'

#ExpectCMD(cdd,"~Saseny")
#ExpectCMD(cdd1,"~Saseny")
#ExpectCMD(cdd2,"~Saseny")
#ExpectCMD(cdd3,"~Saseny")

passwd = "~Saseny"

acm = commands.getstatusoutput('sudo /usr/sbin/asr -partition /dev/disk1 -testsize 70g -retestsize 1g -recoverysize 80g')
#acm = commands.getstatusoutput('expect -c "set timeout 25; spawn sudo /usr/sbin/asr -partition /dev/%s -testsize %s -retestsize %s -recoverysize %s; expect -re \".*password*\";send \"%s\r\";expect -re \"$\";interact"'%("disk1","50g","1g","80g","~Saseny"))
#a,b = commands.getstatusoutput('expect -c "set timeout 25;spawn sudo /usr/sbin/asr -partition /dev/disk1 -testsize 70g -retestsize 1g -recoverysize 80g; expect -re \".*password*\";send \"~Saseny\r\";expect -re \"$\";interact"')
j = acm.expect(['yes/no', 'assword:', '\*',pexpect.EOF], timeout=240)
if j == 1:
	acm.sendline(passwd)
	print 'passwd *********'
elif j == 0:
	acm.sendline('yes\r')
	print 'yes'
	acm.expect('assword:')
	acm.sendline(passwd)
	print 'passwd *********'
elif j == 2:
	print 'unknow'
	print acm.expect('assword:')
	acm.sendline(passwd)
	print 'passwd *********'

