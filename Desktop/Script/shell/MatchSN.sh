#!/bin/sh

SystemSN=`system_profiler SPHardwareDataType | grep "Serial" | sed 's/.*: //'`
SNMessage=`cat < /Volumes/DATA/_UnitsMessage/SN.txt | awk -F ';' '{print$2}'`
for SN in $SNMessage ; do 
if [ $SN == $SystemSN ];then 
echo "\033[32m SN Matched \033[30m"
exit 0
fi 
done
echo;echo "\033[31m No Match SN !!!\033[30m";echo;exit 1