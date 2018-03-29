#!/bin/sh

i=`diskutil list | grep -c "MaxDisk"`

if [ $i -eq 0 ];then 
  echo "不是正常测试硬盘!" ; exit 1
fi  

CheckStates()
{
   if [ $? -eq 0 ];then
      echo "\033[032m $Station : [PASS] \033[030m"
     else
      echo "\033[031m $Station : [FAIL] \033[030m" ; exit 1
   fi
}      

sudo diskutil partitionDisk /dev/disk1 1 GPTFormat HFS+ Diagnostics 1G
Station="diskutil partitionDisk /dev/disk1 1 GPTFormat HFS+ Diagnostics 1G"
CheckStates

sudo /usr/sbin/asr -partition /dev/disk1 -testsize 50g -retestsize 1g -recoverysize 80g
Station="/usr/sbin/asr -partition /dev/disk1 -testsize 50g -retestsize 1g -recoverysize 80g"
CheckStates

diskutil unmountDisk /dev/disk1s3
Station="diskutil unmountDisk /dev/disk1s3"
CheckStates

sudo /usr/sbin/asr -s /Users/saseny/Desktop/Bundle/TestBundle/J79A_Proto1_1-1_15.3A.dmg -t /dev/disk1s3 -erase -noprompt
Station="/usr/sbin/asr -s /Users/saseny/Desktop/Bundle/TestBundle/J79A_Proto1_1-1_15.3A.dmg -t /dev/disk1s3 -erase -noprompt"
CheckStates

diskutil mount disk1s3

cp -rf /Users/saseny/Desktop/Check_SN/Product /Volumes/MaxDisk/Phoenix
Station="cp -rf /Users/saseny/Desktop/Check_SN/Product /Volumes/MaxDisk/Phoenix"
CheckStates

rm -rf /Volumes/MaxDisk/Phoenix/Tables
Station="rm -rf /Volumes/MaxDisk/Phoenix/Tables"
CheckStates

cp -rf /Users/saseny/Desktop/Check_SN/Product/Check_SN/Tables /Phoenix
Station="cp -rf /Users/saseny/Desktop/Check_SN/Product/Check_SN/Tables /Phoenix"
CheckStates

cp -rf /Users/saseny/Desktop/Check_SN/Product/Check_SN/Tables.zip /Phoenix
Station="cp -rf /Users/saseny/Desktop/Check_SN/Product/Check_SN/Tables.zip /Phoenix"
CheckStates

cp -rf /Users/saseny/Desktop/Check_SN/Product/Check_SN/GeneralPreference.plist /Volumes/MaxDisk/Phoenix/Configuration
Station="cp -rf /Users/saseny/Desktop/Check_SN/Product/Check_SN/GeneralPreference.plist /Volumes/MaxDisk/Phoenix/Configuration"
CheckStates

cp -rf /Users/saseny/Desktop/Check_SN/Check_SN.command /Volumes/MaxDisk/private/var/root/Desktop
Station="cp -rf /Users/saseny/Desktop/Check_SN/Check_SN.command /Volumes/MaxDisk/private/var/root/Desktop"
CheckStates

cp -rf /Users/saseny/Desktop/Check_SN/Reset_12_Hours.command /Volumes/MaxDisk/private/var/root/Desktop
Station="cp -rf /Users/saseny/Desktop/Check_SN/Reset_12_Hours.command /Volumes/MaxDisk/private/var/root/Desktop"
CheckStates


echo "[Finished]"