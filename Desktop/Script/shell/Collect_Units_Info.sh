#!/bin/sh

SystemSN=`system_profiler SPHardwareDataType | grep "Serial" | sed 's/.*: //'`
A=";"
if [ -z $SystemSN ];then 
SystemSN=`cat < /Phoenix/Logs/state.txt | grep "WIP" | awk '{print$6}' | awk -F '+' '{print$1}' | grep "C02"`
fi 
Model=`cat < /Phoenix/Logs/state.txt | grep "WIP" | awk '{print$6}' | awk -F '+' '{print$2}'`
echo "\033[32m Pls input the Units Number .... \033[30m"
read UnitsNumber

echo "\033[32m Pls input the Units Config .... \033[30m"
read UnitsConfig
if [ -z $UnitsConfig ];then 
UnitsConfig="Config"
fi

#echo $UnitsNumber ; echo $SystemSN ; echo $Model
INFO1="$UnitsNumber""$A""$SystemSN"
INFO2="$A""$Model""$A""$UnitsConfig"
INFO="$INFO1""$INFO2"
echo $INFO >> /Volumes/DATA/_UnitsMessage/SN.txt