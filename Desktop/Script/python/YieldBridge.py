#!/usr/bin/python

import mysql.connector as dbconnector
import datetime
import time
import os
import sys


f=open('/Users/saseny/Desktop/hd rack/date/d3.tsv','a+')
#Query_start = datetime.datetime(2016,6,14,0,0,0)
Query_start=  time.mktime(time.strptime('2017-06-09 16:00:00', '%Y-%m-%d %H:%M:%S'))
Query_end =  time.mktime(time.strptime('2017-06-12 10:00:00', '%Y-%m-%d %H:%M:%S'))

try:
	#cnx = dbconnector.connect(user='root',host='17.101.7.130',port=3333,database='wabisabi',connection_timeout=60)
	cnx = dbconnector.connect(user='root',host='127.0.0.1',port=3333,database='wabisabi')
	#cnx = dbconnector.connect(user='root',host='127.0.0.1',database='wabisabi')
except dbconnector.Error as err:
	#if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
	#	print("Something is wrong with your user name or password")
	#elif err.errno == errorcode.ER_BAD_DB_ERROR:
	#	print("Database does not exist")
	#else:
	print(err)
	exit(-1)

cursor = cnx.cursor()

def get_FailList():
	global cursor
	global Query_start
	global Query_end
#	query= ("select serial_number from completed_sequences  \
#			where `status` != 'PASSED' and stop_time BETWEEN %d AND %d order by stop_time ASC" %(Query_start,Query_end))
	query= ("select serial_number from completed_sequence  \
			where stop_time BETWEEN %d AND %d order by stop_time ASC" %(Query_start,Query_end))
			
	cursor.execute(query)
	FailList= cursor.fetchall()
	Lookup_List=[]
	for row in FailList:
		if not row[0] in Lookup_List:
			Lookup_List.append(row[0])
	return Lookup_List

def Build_FailHistoricTable():
	global cursor
	global Query_start
	global Query_end
	result_List=[]
	for sn in get_FailList():
		#print sn
		query= ("select FROM_UNIXTIME( a.stop_time, '%%Y/%%m/%%d' ) as `Date`,FROM_UNIXTIME( a.stop_time, '%%H:%%i' ) as `Time`,d.`test_key`, a.serial_number,d.`name`,Replace(a.`summary`,concat(d.`name`,':'),'') as Symptom, e.`rack`,a.slot \
				from completed_sequence as a inner join `unit_action` as b on b.`unit_sequence_id`=a.`unit_sequence` and b.`sequence_action_id`=(select max(sequence_action_id) from `unit_action` where `unit_sequence_id`=a.`unit_sequence`) \
				left join `sequence_action` as c on  b.`sequence_action_id`=c.`id` \
				left join `action` as d on d.id = c.`action_id` \
				left join `slot` as e on e.`sio_slot`=a.`slot` \
         		WHERE  a.serial_number='%s' and a.stop_time BETWEEN %d AND %d order by a.stop_time ASC" %(sn,Query_start,Query_end))
		cursor.execute(query)
		Table= cursor.fetchall()
		
# 		Listlength=len(Table)
# 		for i in range(0,Listlength):
# 			if i != Listlength-1:  	#test key 
# 				if result_List[i][3] == result_List[i+1][3] and result_List[i][4] == result_List[i+1][4]: #fail Symptom		
# 					result_List.append([list(row),'Fail Same Test'])
# 				elif result_List[i][4] == 'Completed successfully':
# 					result_List.append([list(row),'Pass'])
# 			elif result_List[i][4] == 'Completed successfully':
# 				result_List.append([list(row),'Pass'])
# 			else
# 				result_List.append([list(row),'Fail'])

		for row in Table:
			result_List.append(list(row))
#		Listlength=len(Table)
# 		for i in range(0,Listlength):
# 			if 	result_List[i][4] == 'Completed successfully':
# 				result_List.append([list(row),'Pass'])
# 			else:
# 				result_List.append([list(row),'Fail'])
		
	return result_List


InputQuery = ("select status from unit where last_ping BETWEEN %d AND %d" %(Query_start,Query_end))
cursor.execute(InputQuery)
Npassed=0
Nfailed=0
for (status,) in cursor:
 	if status == 'Passed':
 		Npassed=Npassed+1
 	else:
 		Nfailed=Nfailed+1

for (date,stop_time,test_key,serial_number,name,Symptom,rack,slot) in Build_FailHistoricTable():
 	f.write("%s\t%s\t%s\t%s\t%s\t%s\t%d\t %d" % (date,stop_time,test_key,serial_number,name,Symptom,rack,slot))
 	f.write('\n') 
 
f.close()
# f.write("Test %d, Pass %d, Fail %d, yield %.3f" %(Npassed+Nfailed,Npassed,Nfailed,float(Npassed)/(Npassed+Nfailed)))
# f.write('\n')
# #query = "select stop_time,slot from completed_sequences"
# query = 	("select FROM_UNIXTIME( a.stop_time, '%%Y/%%m/%%d-%%H:%%i' ) as `Time`,d.`test_key`, a.serial_number,d.`name`,Replace(a.`summary`,concat(d.`name`,':'),'') as Symptom, concat('Rack',e.`rack`,'-',a.slot) as Station,f.`status` \
# 			from completed_sequences as a inner join `unit_action` as b on a.`unit_sequence`=b.`unit_sequence_id` and b.`status_id`!=1 \
# 			left join `sequence_action` as c on  b.`sequence_action_id`=c.`id` \
# 			left join `action` as d on d.id = c.`action_id` \
# 			left join `slots` as e on e.`sio_slot`=a.`slot` \
# 			left join units as f on a.`serial_number`=f.`serial_number` \
#          	WHERE a.stop_time BETWEEN %d AND %d order by a.stop_time ASC" %(Query_start,Query_end))
# #cursor.execute(query, (Query_start, Query_end))
# cursor.execute(query)
# 
# FailTable= cursor.fetchall()
# #print len(cursor.fetchall())
# Lookup_List=[]
# result_List=[]
# for (stop_time,test_key,serial_number,name,Symptom,Station,status) in FailTable:
# 	if not serial_number in Lookup_List:
# 		Lookup_List.append(serial_number)
# 		#for (stop_time1,test_key1,serial_number1,name1,Symptom1,Station1,status1) in FailTable:
# 		for row in FailTable:
# 			if  row[2] == serial_number:
# 				result_List.append(list(row))
# 				#print("%s, %s" % (serial_number, name))
# 
# Listlength=len(result_List)
# for i in range(0,Listlength):
# 	if i != Listlength-1 and result_List[i][2] ==  result_List[i+1][2]:  	#test key 
# 		if result_List[i][1] == result_List[i+1][1] and result_List[i][4] == result_List[i+1][4]: #fail Symptom
# 			result_List[i][6] = 'Fail Same Test'
# 		else:
# 			result_List[i][6] = 'Fail Different Test'
# 	else:
# 		if 	result_List[i][6] == 'PASSED':
# 			result_List[i][6] = 'Pass'
# 		else:
# 			result_List[i][6] = 'Fail'
#  			
# for (stop_time,test_key,serial_number,name,Symptom,Station,status) in result_List:
# 	f.write("%s\t%s\t%s\t%s\t%s\t%s\t%s" % (stop_time,test_key,serial_number,name,Symptom,Station,status))
# 	f.write('\n')
# #cursor.close()
# #cnx.close()
