#!/bin/sh
#set -x
SystemSN=`system_profiler SPHardwareDataType | grep "Serial" | sed 's/.*: //'`
Model_TB=`cat /Volumes/DATA/_UnitsMessage/SN.txt | grep "$SystemSN" | awk -F ';' '{print$3}'`
WIP="$SystemSN"+"$Model_TB"
sleep 1
echo "\033[32m $WIP \033[30m"
touch /private/var/root/Desktop/$WIP
