#!/bin/sh

#  ForLogCheck.sh
#  testv
#
#  Created by Saseny on 12/28/16.
#  Copyright © 2016 Saseny. All rights reserved.

Date=`date +%Y%m%d_%H%M%S`
logExitsPath
if [ -z $1 ];then
   logPath="$SCRIPT_DIR/DATALog" ; echo "[LogPath: $logPath]"
else
   logPath="$1" ; echo "[LogPath: $1]"
fi
resultPath="$SCRIPT_DIR/$Dat
resultPathe.csv"
tmepPath="$SCRIPT_DIR/tmp"
  
Total=`ls -n $logPath | grep -c "Dec"`
allLogFinder=`ls $logPath`

echo "DATE, TIMES, SN, USE TIME, TEST USE TIME, ASR_bandwidth, CM USE TIME, CM_Copy_bandwitdth, Partition Time, LINE, Station, FixtureSlotID, BeginTime, EndTime, TEST Name, TEST Size, CM Name, CM Size, WIP, PCIBridge, DCSD_Serial_Number, DriveDuplicator Host SN, PCIeSlot" >> $resultPath 

for oneLog in $allLogFinder
do
       mkdir -p $tmepPath
       cp -rf $logPath/$oneLog $tmepPath
       cd $tmepPath
       gunzip $oneLog
       
       logName=`echo $oneLog | awk -F '.gz' '{print$1}'`
       
       DateTime=`cat < $tmepPath/$logName | head -1 | awk -F '.' '{print$1}' | sed 's/\[//g' | awk '{print$1}'`
       BeginTime=`cat < $tmepPath/$logName | head -1 | awk -F '.' '{print$1}' | awk -F '[' '{print$2}'`
       EndTime=`cat < $tmepPath/$logName | tail -1 | awk -F '.' '{print$1}' | awk -F '[' '{print$2}'`
       PCIBridge=`cat < $tmepPath/$logName | grep "PCIBridge" | sed 's/.*= //' | sed 's/..$//' | sed 's/^.//'`
       PCIeSlot=`cat < $tmepPath/$logName | grep "PCIeSlot" | sed 's/.*= //' | sed 's/..$//' | sed 's/^.//' | head -1`
       DCSD_Serial_Number=`cat < $tmepPath/$logName | grep "DCSD Serial Number" | sed 's/.*= //' | sed 's/.$//'`
       FixtureSlotID=`cat < $tmepPath/$logName | grep "FixtureSlotID" | sed 's/.*= //' | sed 's/.$//'`
       SerialNumber=`cat < $tmepPath/$logName | grep "WIPSerialNumber" | head -1 | sed 's/.*= //' | sed 's/\;//'`
       HostSN=`cat < $tmepPath/$logName | grep "DriveDuplicator Host SN:" | sed 's/.*: //' | sed 's/\[//g' | sed 's/\]//g'`
       TestBundle=`cat < $tmepPath/$logName | grep "TestImages" | awk -F '.dmg' '{print$1}' | sed 's/.*\///'`
       WIP=`cat < $tmepPath/$logName | grep "WIPBarcod" | head -1 | awk -F ';' '{print$1}' | sed 's/.*\= //' | sed 's/"//g'`
       CMimage=`cat < $tmepPath/$logName | grep "CM image" | awk -F '.dmg]' '{print$1}' | sed 's/.*\[//'`
       TestBundleDownloadTime=`cat < $tmepPath/$logName | grep "Test Image Restore" | sed 's/.*= //'`
       CMbundleDownloadTime=`cat < $tmepPath/$logName | grep "CM Copy" | sed 's/.*= //' | head -1`       
       Overall=`cat < $tmepPath/$logName | grep "Overall" | sed 's/.*= //'`
       Partition=`cat < $tmepPath/$logName | grep "Partition =" | sed 's/.*= //'`
       TestBundleSize=`cat < $tmepPath/$logName | grep "Test Bundle size =" | sed 's/.*= //'`
       CMBundleSize=`cat < $tmepPath/$logName | grep "CM Bundle size =" | sed 's/.*= //'`
       ASR_bandwidth=`cat < $tmepPath/$logName | grep "ASR bandwidth =" | sed 's/.*= //'`
       CM_Copy_bandwitdth=`cat < $tmepPath/$logName | grep "CM Copy bandwitdth =" | sed 's/.*= //'`
       Line=`cat < $0 | grep "$HostSN" | awk '{print$2}'`
       Station=`cat < $0 | grep "$HostSN" | awk '{print$4}'`
       
       [ -z $CMimage ] && CMimage="Did not Download"
       
       outPutMessage="$DateTime,$downLoadTimes,$SerialNumber,$Overall,$TestBundleDownloadTime,$ASR_bandwidth,$CMbundleDownloadTime,$CM_Copy_bandwitdth,$Partition,$Line,$Station,$FixtureSlotID,$BeginTime,$EndTime,$TestBundle,$TestBundleSize,$CMimage,$CMBundleSize,$WIP,$PCIBridge,$DCSD_Serial_Number,$HostSN,$PCIeSlot" 
       
       downLoadTimes=`ls $logPath | grep -c "$SerialNumber"`
       
       if [ $downLoadTimes -gt 1 ];then
           echo 1 >> $SCRIPT_DIR/count.log
           count=`cat < $SCRIPT_DIR/count.log | grep -c "1"`          
           if [ $count -eq $downLoadTimes ];then                          
             echo $outPutMessage >> $resultPath
             rm -rf $SCRIPT_DIR/count.log
           fi     
         else              
           echo $outPutMessage >> $resultPath 
       fi    
       
       let Total-=1       
       echo "[($Total)]"    
       [ $Total -eq 0 ] && echo "FINISHED!"
                 
       rm -rf $tmepPath
done    
rm -rf $SCRIPT_DIR/count.log
#sleep 3
#cd $SCRIPT_DIR
#sort -t, -k1n -o Modify_SWDL.csv $Date.csv
  
  




