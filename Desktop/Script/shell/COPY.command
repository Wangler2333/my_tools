#!/bin/sh

SN=`cat < /Phoenix/Logs/SerialNumber.txt`
SerNum=`system_profiler SPHardwareDataType | grep "Serial Number" | sed 's/.*: //'`
DATE=`date +%Y_%m_%d@%H-%M-%S`
SN1="$SN"@"$DATE"
SN2="$SerNum"_"$DATE"

mkdir /Volumes/Download/Logs/$SN
/Volumes/Download/Command/TE_Support/Tools/Phoenix/COPYLOGS_PRE.pl
sleep 1
screencapture /Volumes/Download/Logs/$SN/PreFail.png
sleep 1
#/Volumes/Download/Command/Test_Process/Collect_PreData.pl
mv -rf /private/var/root/Desktop/*.tgz /Volumes/Download/Logs/$SN
sleep 1
cp -rf /private/var/root/Desktop/Preburn /Volumes/Download/Logs/$SN
cd /Volumes/Download/Logs/$SN
mv Preburn $SN
zip -r $SN1.zip $SN
