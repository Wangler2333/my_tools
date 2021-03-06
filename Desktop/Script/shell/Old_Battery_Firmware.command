#!/bin/sh
Expected="702"
System_SN=`system_profiler SPHardwareDataType | grep "Serial Number" | sed 's/.*: //'`
Bundle=`ls /Phoenix/Tables | grep "PGQ" | awk -F '.tb*' '{print$1}' | awk -F '_' '{print$3}'`
Battery_FW=`system_profiler SPPowerDataType | grep "Firmware Version" | sed 's/.*: //'`
Time=`date +%y-%m-%d\ %H:%M:%S`

Path="/Volumes/DATA/Old_Battery_FW/Modify_Units_Info.txt"
Number=`cat < /Volumes/DATA/Old_Battery_FW/Modify_Units_Info.txt | grep -c "C02"`
Number_=`expr $Number + 1`

Return="[ NO. $Number_ ][ Battery_FW : $Battery_FW ] [ Bundle Version : $Bundle ] [ Modify Time : $Time ] [ Serial Number : $System_SN ]"
if [ `ls /Volumes/DATA/Old_Battery_FW | grep -c "Modify_Units_Info.txt"` -eq 0 ]; then
  echo "---------------------------------------------------------------------------------------------------------------------------" >> $Path 
  echo "[ Number ] [ Battery Fireware ] [  Bundle Version  ] [      Modified Tables Time       ] [     System Serial Number     ]" >> $Path 
  echo "---------------------------------------------------------------------------------------------------------------------------" >> $Path 
fi
 
echo $Return >> $Path 
if [ $Battery_FW != $Expected ]; then 
   echo "\033[31m Not Old Battery Firmware Units , Pls check it and Re-download Expected Bundle... \033[30m"
   exit 0
fi   
echo "\033[32m [ Battery_FW : $Battery_FW ] [ Bundle Version : $Bundle ] \033[30m"
#rm -rf /Phoenix/Tables ; sleep 1
#cp -rf /Volumes/DATA/Old_Battery_FW/Tables /Phoenix ; sleep 1
#/TE_Support/Tools/Phoenix/cleanup_Phoenix2.command ; sleep 1
#reboot