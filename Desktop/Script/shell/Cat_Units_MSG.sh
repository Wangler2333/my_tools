#!/bin/sh

SystemSN=`system_profiler SPHardwareDataType | grep "Serial" | awk -F ':' '{print$2}'`
B="\n"
Date=`date +%Y-%m-%d--%H:%M:%S`

if [ -z $SystemSN ];then 
SystemSN=`cat < /Phoenix/Logs/state.txt | grep "WIP" | awk '{print$6}' | awk -F '+' '{print$1}'`
fi 
WIP=`cat < /Phoenix/Logs/state.txt | grep "WIP" | awk '{print$6}'`
echo "$WIP"

echo $WIP >> /Volumes/DATA/x21_Units/Units_Info.txt
echo $Date >> /Volumes/DATA/x21_Units/Units_Info.txt
echo $B >> /Volumes/DATA/x21_Units/Units_Info.txt

sleep 1
/Volumes/DATA/_ReCopy.command 