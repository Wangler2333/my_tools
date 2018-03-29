#!/bin/sh

#  ForLogCheck.sh
#  testv
#
#  Created by Saseny on 12/28/16.
#  Copyright © 2016 Saseny. All rights reserved.
#  Need Default File

Date=`date +%Y%m%d_%H%M%S`
SCRIPT_DIR=`dirname $0`

# Default File Path and check File Exist.
DefaultPath="/Users/saseny/Desktop/Script_Command"
DefaultFilePath="/Users/saseny/Desktop/Script_Command/DefaultFile.txt"
if [ `ls $DefaultPath | grep -c "DefaultFile.txt"` -eq 0 ];then
   echo "Default File is not Exits."
fi
# Debug yes or not
#if [ `cat < $DefaultFilePath | grep "Debug" | sed 's/.*=//'` -eq 1 ];then
#   set -x
#fi   
# Log Path Default Set or $1, and $1 first.
if [ -z $1 ];then
   logExitsPath=`cat < $DefaultFilePath | grep "logExitsPath" | sed 's/.*=//'`
 else
   logExitsPath=$1
fi

# Result File Path and check, if not exist then set result path as same as script path.
resultPath=`cat < $DefaultFilePath | grep "resultPath" | sed 's/.*=//'`
#if [ $resultPath -eq 0 ];then
#   resultPath="$SCRIPT_DIR/Date.csv"
#fi

logTotal=`ls -n $logExitsPath | grep -c "Dec"`
allLog=`ls $logExitsPath`

# Output catalogue
echo "DATE, Serial Number, WIP, Line, FixtureSlotID, Station, Test Bundle Name, Test Bundle Use Time, Customer Bundle, Customer Bundle Use Time, Parttion Time, Download Times " >> $resultPath

for oneLog in $allLog
do

     mkdir -p /tmp/logcheck
     cp -rf $logExitsPath/$oneLog /tmp/logcheck
     cd /tmp/logcheck
     gunzip $oneLog

     logName=`echo $oneLog | awk -F '.gz' '{print$1}'`

     DateTime=`cat < /tmp/logcheck/$logName | head -1 | awk '{print$1,$2}'`
#     BeginTime=`cat < /tmp/logcheck/$logName | head -1 | awk -F '.' '{print$1}' | awk -F '[' '{print$2}'`
#     EndTime=`cat < /tmp/logcheck/$logName | tail -1 | awk -F '.' '{print$1}' | awk -F '[' '{print$2}'`
#     PCIBridge=`cat < /tmp/logcheck/$logName | grep "PCIBridge" | sed 's/.*= //' | sed 's/..$//' | sed 's/^.//'`
#     PCIeSlot=`cat < /tmp/logcheck/$logName | grep "PCIeSlot" | sed 's/.*= //' | sed 's/..$//' | sed 's/^.//' | head -1`
#     DCSD_Serial_Number=`cat < /tmp/logcheck/$logName | grep "DCSD Serial Number" | sed 's/.*= //' | sed 's/.$//'`
     FixtureSlotID=`cat < /tmp/logcheck/$logName | grep "FixtureSlotID" | sed 's/.*= //' | sed 's/.$//'`
     SerialNumber=`cat < /tmp/logcheck/$logName | grep "WIPSerialNumber" | head -1 | sed 's/.*= //' | sed 's/\;//'`
     HostSN=`cat < /tmp/logcheck/$logName | grep "DriveDuplicator Host SN:" | sed 's/.*: //' | sed 's/\[//g' | sed 's/\]//g'`
     TestBundle=`cat < /tmp/logcheck/$logName | grep "TestImages" | awk -F '.dmg' '{print$1}' | sed 's/.*\///'`
     WIP=`cat < /tmp/logcheck/$logName | grep "WIPBarcod" | head -1 | awk -F ';' '{print$1}' | sed 's/.*\= //' | sed 's/"//g'`
     CMimage=`cat < /tmp/logcheck/$logName | grep "CM image" | awk -F '.dmg]' '{print$1}' | sed 's/.*\[//'`
     TestBundleDownloadTime=`cat < /tmp/logcheck/$logName | grep "Test Image Restore" | sed 's/.*= //'`
     CMbundleDownloadTime=`cat < /tmp/logcheck/$logName | grep "CM Copy" | sed 's/.*= //' | head -1`
     Overall=`cat < /tmp/logcheck/$logName | grep "Overall" | sed 's/.*= //'`
     Partition=`cat < /tmp/logcheck/$logName | grep "Partition =" | sed 's/.*= //'`
#     TestBundleSize=`cat < /tmp/logcheck/$logName | grep "Test Bundle size =" | sed 's/.*= //'`
#     CMBundleSize=`cat < /tmp/logcheck/$logName | grep "CM Bundle size =" | sed 's/.*= //'`
#     ASR_bandwidth=`cat < /tmp/logcheck/$logName | grep "ASR bandwidth =" | sed 's/.*= //'`
#     CM_Copy_bandwitdth=`cat < $tmepPath/$logName | grep "CM Copy bandwitdth =" | sed 's/.*= //'`
     Line=`cat < $DefaultFilePath | grep "$HostSN" | awk '{print$2}'`
     Station=`cat < $DefaultFilePath | grep "$HostSN" | awk '{print$4}'`

          [ -z $CMimage ] && CMimage="Didn't Download"

          outPutMessage="$DateTime,$SerialNumber,$WIP,$Line,$FixtureSlotID,$Station,$TestBundle,$TestBundleDownloadTime,$CMimage,$CMbundleDownloadTime,$Partition,$Overall"

          downLoadTimes=`ls $logExitsPath | grep -c "$SerialNumber"`



          if [ $downLoadTimes -gt 1 ];then
              echo 1 >> /tmp/count.log
              count=`cat < $SCRIPT_DIR/count.log | grep -c "1"`
            if [ $count -eq $downLoadTimes ];then
                echo $outPutMessage >> $resultPath
                rm -rf /tmp/count.log
            fi
           else
              echo $outPutMessage >> $resultPath
          fi

              let Total-=1
              echo "\* $Total \*"
              [ $Total -eq 0 ] && echo "FINISHED!"

            rm -rf /tmp/logcheck
done
rm -rf $/tmp/count.log





