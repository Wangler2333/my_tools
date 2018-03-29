#!/usr/bin/python

import datetime
import time
import os
import sys
import pexpect3_2.pexpect as pexpect
import re

#Query_start = datetime.datetime(2016,6,14,0,0,0)
Query_start=  time.mktime(time.strptime('2016-6-13 00:00:00', '%Y-%m-%d %H:%M:%S'))
Query_end =  time.mktime(time.strptime('2020-12-31 00:00:00', '%Y-%m-%d %H:%M:%S'))


def loginSSH(ip,user, passwd):
	ssh = pexpect.spawn('ssh %s@%s' % (user,ip))
	print 'ssh %s@%s' % (user,ip)
	try:
		i = ssh.expect(['yes/no', 'assword:', '\*',pexpect.EOF], timeout=60)
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
	
	try:
		ssh.expect('QSMC', timeout=10)
	except pexpect.TIMEOUT:
		print "login TIMEOUT"
		ssh.close()
		exit(-3)
	return ssh

def pfSSH(ssh,ip,user, passwd):
	ssh.sendline('ssh -L 3333:localhost:3306 %s@%s' % (user,ip))
	print 'ssh -L 3333:localhost:3306 %s@%s' % (user,ip)
	try:
		i = ssh.expect(['yes/no', 'assword:',pexpect.EOF], timeout=30)
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
		print "TIMEOUT"
		ssh.close()
		exit(-2)
	return ssh
    
def runCMD(ssh,cmd,silence=False):
	ssh.sendline(cmd)
	if not silence:
		ssh.sendline('echo $HOSTNAME')
		try:
			i=ssh.expect(['NAND-STATS.local','NAND-STATS-2.local'],timeout=10)
			#ssh.expect('NAND-STATS',timeout=10)
			print ssh.before,ssh.after
			print "==========================================================="
		except pexpect.EOF:
			print "EOF"
		except pexpect.TIMEOUT:
			print "runCMD TIMEOUT"
def getIPlist():
	ipList=[]
	pwd = sys.path[0]
	f=open(pwd + '/IP.txt','r')
	for line in f:
		tx=line.strip()
		if (not tx.startswith('#')) and len(tx)>8:
			cc = tx.split('#')
			ipList.append(cc[0].strip())
	return ipList

def getEEEElist():
        ipList=[]
        pwd = sys.path[0]
        f=open(pwd + '/EEEE.txt','r')
        for line in f:
                tx=line.strip()
                if (not tx.startswith('#')) and len(tx)==4:
                        ipList.append(tx)
        return ipList


#sql="SELECT s.id AS slot_id, c.state_id AS carrier_state_id, u.serial_number AS unit, u.state_id AS unit_state_id, (unix_timestamp() - u.last_ping) AS last_ping, us.id as seq_id,us.dur as test_duration,ua.id as action_id, u.status AS statu \
#FROM carrier as c join slot_and_carrier as sac on sac.carrier_id = c.id \
#left join carrier_and_unit as cau on cau.carrier_id = c.id \
#left join unit as u on u.id = cau.unit_id  \
#left join slot as s on s.id = sac.slot_id \
#left join (select id,unit_id, (unix_timestamp()- max(start_time))/3600 as dur from unit_sequence group by unit_id )  us on us.unit_id=u.id \
#left join unit_action as ua on ua.unit_sequence_id=us.id and ua.stop_time is NULL \
#where c.state_id !=10 and c.state_id !=8 and u.serial_number is not NULL and us.dur>18 \
#ORDER BY test_duration DESC"


for ip in getIPlist():
	ssh = loginSSH(ip,'gdadmin','gdadmin')
	eeeeList=getEEEElist()
	#print eeeeList
	for eeee in eeeeList:
		sql="INSERT INTO configuration (code, sequence_id, product_id) VALUES ('%s', 2, 81)" % (eeee)
		#print '/usr/local/mysql/bin/mysql -u root  wabisabi -e "%s"' % (sql)
		runCMD(ssh, '/usr/local/mysql/bin/mysql -u root  wabisabi -e "%s"' % (sql),True )
	sql="select * from configuration ORDER BY id DESC LIMIT %d" % (len(eeeeList))
	#print '/usr/local/mysql/bin/mysql -u root  wabisabi -e "%s"' % (sql) 
	runCMD(ssh, '/usr/local/mysql/bin/mysql -u root  wabisabi -e "%s"' % (sql) )
	ssh.close()
