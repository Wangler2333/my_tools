#!/bin/sh
DATE=`date +%Y%m%d_%H%M%S`
###########update Product and Buildstage as need############
SN=$(system_profiler SPHardwareDataType | grep Serial | sed 's/.*://g')
logfile=~/Desktop/Shutdwon_Check_"$SN".txt
echo $DATE > $logfile
system_profiler SPHardwareDataType >> $logfile
log=/var/log/system.log
cat $log | grep "shutdown cause" >> $logfile 

if [ `cat $log | grep -c "shutdown cause: 0"` -gt 0 ];then
	echo   "\033[41;33m Found Force Shutdown!!\033[1m"
	exit 1
else 
	echo "\033[32m Shutdown is clean!\033[0m"
fi
exit 0



