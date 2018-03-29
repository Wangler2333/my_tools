#!/bin/sh

Source="/Volumes/DATA/11.22/state.txt"
Aim1="/Users/saseny/Desktop/state.txt"
Aim2=


Message()
{
SystemSN=`system_profiler SPHardwareDataType | grep "Serial" | sed 's/.*: //'`
Model_TB=`cat /Volumes/DATA/_UnitsMessage/SN.txt | grep "$SystemSN" | awk -F ';' '{print$3}'`
WIP="$SystemSN"+"$Model_TB"
EEcode=`echo $SystemSN | tail -c 5`
}

Change()   ## Change SerialNumber.txt
{
echo $SystemSN > $Aim2
}


cat < $Source | head -5 > $Aim
Message

Row1="3 WIP 10 StringType 22 $WIP"
Row2="16 SalesOrderNumber 10 StringType 9 $Model_TB"
Row3="6 HWCode 10 StringType 4 $EEcode"
Row4="12 SerialNumber 10 StringType 12 $SystemSN"

echo $Row1 >> $Aim ; echo $Row2 >> $Aim ; echo $Row3 >> $Aim ; echo $Row4 >> $Aim 
cat < $Source | tail -4 >> $Aim

Change