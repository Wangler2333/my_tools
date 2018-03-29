#!/bin/sh

#########################################################
# Use command to check the failure is caused by process #
#########################################################

R1=`cat /Phoenix/Logs/processlog.plog | grep -c 'ACEN is 0 and not as expected 1'`
R2=`cat /Phoenix/Logs/processlog.plog | grep -c 'Fail_Type_Str="Hang"'`
R3=`cat /Phoenix/Logs/processlog.plog | grep -c 'Wake reason EC.ACDetach does not match expected wake reason'`
R4=`cat /Phoenix/Logs/processlog.plog | grep -c 'Wake reason SPIT does not match expected wake reason'`
R5=`cat /Phoenix/Logs/processlog.plog | grep -c 'Wake reason EC.PowerButton PWRB does not match expected wake reason'`
R6=`cat /Phoenix/Logs/processlog.plog | grep -c '/Users/diagscmB/Bristol_Sources/Battery/Battery/Tests/BatteryChargeTerminationTest.m, line: 58, assertion: aConnected'`
R7=`cat /Phoenix/Logs/processlog.plog | grep -c 'Wake reason EC.PME does not match expected wake reason'` 

if [ "${R1}" -ne 0 ] || [ "${R2}" -ne 0 ] || [ "${R3}" -ne 0 ] || [ "${R4}" -ne 0 ] || [ "${R5}" -ne 0 ] || [ "${R6}" -ne 0 ] || [ "${R7}" -ne 0 ];then
	echo "Process Issue !"
	open /TE_Support/Images/Failure_Check.jpg	
	exit 1
			
else 
	echo "No Process Issue !"
	exit 0
fi