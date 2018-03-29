#!/bin/sh
#set -x
Time=`date +%y-%m-%d\.%H:%M:%S`
TBTFW=`system_profiler SPThunderboltDataType | grep "Firmware Version:" | head -1 | sed 's/.*: //'`

cd /Volumes/DATA/_Script
chmod +x Transitive.sh
/Volumes/DATA/_Script/Transitive.sh 
/Volumes/DATA/_Script/Touch_WIP.sh
/Volumes/DATA/_Script/Touch_Units_Number.sh
/Volumes/DATA/_Script/Rename_USB.sh
if [ -f /*.dmg ];then 
/Volumes/DATA/_Script/Touch_CM_Number.sh
fi

if [ `ls /Volumes/DATA/Tools | grep -c "Tables"` -eq 1 ];then
rm -rf /Phoenix/Tables 
[ $? -eq 0 ] && echo "\033[032m[RmPass]\033[030m"
[ $? -eq 1 ] && (echo "\033[031m[RmFail]\033[030m" ; exit 1)
cp -rf /Volumes/DATA/Tools/Tables /Phoenix
[ $? -eq 0 ] && echo "\033[032m[CopyPass]\033[030m"
[ $? -eq 1 ] && (echo "\033[031m[CopyFail]\033[030m" ; exit 1)
/TE_Support/Tools/Phoenix/cleanup_Phoenix2.command 
/TE_Support/Tools/Phoenix/cleanup_Phoenix2.command ; sleep 1
fi

#/Volumes/DATA/_Script/Change_File.sh   ## change some file
#touch /private/var/root/Desktop/$Time  ## Touch Modify Time

#echo "DATE, TIME, SerialNumber, TestBundle, CM-Bundle, ModelNumber" >> /Volumes/DATA/_UnitsMessage/Regression_Info.csv
CM_Bundle=`ls /*.dmg | awk -F '.dmg' '{print$1}'`
SystemSN=`system_profiler SPHardwareDataType | grep "Serial" | sed 's/.*: //'`
Model_TB=`cat /Volumes/DATA/_UnitsMessage/SN.txt | grep "$SystemSN" | awk -F ';' '{print$3}'`
DATE=`date +%Y%m%d`
Time=`date +%H:%M:%S`
TestBundle=`ls /Volumes/DATA/Tools/Tables | grep ".tbproj3" | awk -F '.tbproj3' '{print$1}'`
echo "$DATE, $Time, $SystemSN, $TestBundle, $CM_Bundle, $Model_TB" >> /Volumes/DATA/_UnitsMessage/Regression_Info.csv

case $TBTFW in 
*11.9*)
  echo "TBT FW OK!"
  ;;
*15.4*)
  echo ; echo "\033[031m Need Modify ModelFW File... Pls Check.... \033[030m" ; echo 
  exit 1
  ;;
esac    

if [ ! -f /TE_Support/Tools/Phoenix/Unmount_Lunch.sh ];then
   cp -rf /Volumes/DATA/_Script/Unmount_Lunch.sh /TE_Support/Scripts/Test_Process   
fi   

open -a "/Applications/Utilities/Terminal.app" /TE_Support/Scripts/Test_Process/Unmount_Lunch.sh