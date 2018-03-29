#!/bin/sh
#set -x
SystemSN=`system_profiler SPHardwareDataType | grep "Serial" | sed 's/.*: //'`
Units_Number=`cat /Volumes/DATA/_UnitsMessage/SN.txt | grep "$SystemSN" | awk -F ';' '{print$1}'`
sleep 1
echo "\033[32m $Units_Number \033[30m"
touch /private/var/root/Desktop/$Units_Number
