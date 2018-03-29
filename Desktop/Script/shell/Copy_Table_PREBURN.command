#!/bin/sh

Location="_Pre-Burn"      ##  _Pre-Burn  _Run-In  _Post-Burn
SystemSN=`system_profiler SPHardwareDataType | grep Serial |awk -F ':' '{print$2}'`
UN=`cat < /Volumes/DATA/_UnitsMessage/SN.txt | grep $SystemSN`
Bundle_V=`ls /Phoenix/Tables | grep "PGQ" | awk -F '.tb*' '{print$1}'`
Bundle="Bundle:""$Bundle_V"
Date=`date +%Y-%m-%d--%H:%M:%S`
Start_Mesg="Start Time :""$Date"
B="\n"
Location_=`echo $Location | awk -F '_' '{print$2}'`

rm -rf /Phoenix/Tables
sleep 1
/TE_Support/Tools/Phoenix/cleanup_Phoenix2.command
sleep 1
cp -rf /Volumes/DATA/Tables/Preburn/Tables  /Phoenix

echo $Location_ >> /Volumes/DATA/Tables/Preburn/Regression.txt
echo $UN >> /Volumes/DATA/Tables/Preburn/Regression.txt
echo $Start_Mesg >> /Volumes/DATA/Tables/Preburn/Regression.txt
echo $Bundle >> /Volumes/DATA/Tables/Preburn/Regression.txt
echo $B >> /Volumes/DATA/Tables/Preburn/Regression.txt

sleep 1
cd /Volumes/DATA/_Script
chmod 777 Touch_WIP.sh
cd /private/var/root/Desktop
/Volumes/DATA/_Script/Touch_WIP.sh
sleep 1
#reboot
sleep 1
/TE_Support/Tools/Phoenix/cleanup_Phoenix2.command
sleep 2
reboot