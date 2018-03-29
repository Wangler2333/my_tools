#!/bin/sh

Location="_Run-in"      ##  _Pre-Burn  _Run-In  _Post-Burn
SystemSN=`system_profiler SPHardwareDataType | grep Serial | awk -F ':' '{print$2}'`
UN=`cat < /Volumes/DATA/_UnitsMessage/SN.txt | grep $SystemSN`
Bundle_V=`ls /Phoenix/Tables | grep "PGQ" | awk -F '.tb*' '{print$1}'`
Bundle="Bundle:""$Bundle_V"
Date=`date +%Y-%m-%d--%H:%M:%S`
Start_Mesg="Start Time :""$Date"
CM_Bundle=`ls /*.dmg | awk -F '.dmg' '{print$1}'`
CM_Bundle_="CM_Bundle:""$CM_Bundle"
B="\n"
Location_=`echo $Location | awk -F '_' '{print$2}'`

rm -rf /Phoenix/Tables
sleep 1
/TE_Support/Tools/Phoenix/cleanup_Phoenix2.command
sleep 1
cp -rf /Volumes/DATA/Tables/Runin/Tables  /Phoenix

echo $Location_ >> /Volumes/DATA/Tables/Runin/Regression.txt
#echo $UN >> /Volumes/DATA/Tables/Runin/Regression.txt
echo $Start_Mesg >> /Volumes/DATA/Tables/Runin/Regression.txt
echo $Bundle >> /Volumes/DATA/Tables/Runin/Regression.txt
echo $CM_Bundle_ >> /Volumes/DATA/Tables/Runin/Regression.txt
echo $B >> /Volumes/DATA/Tables/Runin/Regression.txt

sleep 1
cd /Volumes/DATA/_Script
chmod 777 Touch_WIP.sh
cd /private/var/root/Desktop
/Volumes/DATA/_Script/Touch_WIP.sh
touch /private/var/root/Desktop/$CM_Bundle
sleep 1
#reboot