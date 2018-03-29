#!/bin/bash

SCRIPT_DIR=`dirname $0`
logPathRoad="$SCRIPT_DIR/DOWNLOAD"
tempPath="$SCRIPT_DIR/tmp"
resultFile="$SCRIPT_DIR/Runin_time.csv"

allLog=`ls $logPathRoad`
totalNumber=`ls -n $logPathRoad | grep -c "Dec"`

echo "Serial Number, GenuineIntel, Memory, Storage, KB/TP Language, run_inBeginTime, run_inEndTime" >> $resultFile

for oneLog in $allLog
do     
       mkdir -p $tempPath
       cp -rf $logPathRoad/$oneLog $tempPath
       cd $tempPath
       tar -zxvf $tempPath/$oneLog 
       rm -rf $tempPath/$oneLog 
       
       serialNumber=`echo $oneLog | awk -F '_' '{print$1}'`
       logName=`echo $oneLog | awk -F '.tgz' '{print$1}'`
       

       Storage=`cat < $tempPath/$logName/_PHOENIX_CONFIGURATION/Configuration/configExpected.txt | grep "Storage" | awk -F '=' '{print$2}' | awk -F '&' '{print$1}' | sed 's/"//g'`
       GenuineIntel=`cat < $tempPath/$logName/_PHOENIX_CONFIGURATION/Configuration/configExpected.txt | grep "GenuineIntel" | awk -F '=' '{print$3}' | awk -F '&' '{print$1}' | sed 's/"//g'`
       Memory=`cat < $tempPath/$logName/_PHOENIX_CONFIGURATION/Configuration/configExpected.txt | grep "Memory" | awk -F '=' '{print$2}' | awk -F '&' '{print$1}' | sed 's/"//g'`
       Keyboard=`cat < $tempPath/$logName/_PHOENIX_CONFIGURATION/Configuration/configExpected.txt | grep "Keyboard" | tail -1 | awk -F '=' '{print$3}' | awk -F '&' '{print$1}' | sed 's/"//g'`

       run_inBeginTime=`cat < $tempPath/$logName/_PHOENIX_LOGS_PROCESSLOG.PLOG/processlog.plog | grep "CM_Bundle_Verify" | head -1 | awk -F ',' '{print$2}' | sed 's/.*=//' | sed 's/"//g'`
       run_inEndTime=`cat < $tempPath/$logName/_PHOENIX_LOGS_PROCESSLOG.PLOG/processlog.plog | grep "MSD.ntab" | tail -1 | awk -F ',' '{print$2}' | sed 's/.*=//' | sed 's/"//g'`
       
       let totalNumber-=1
       echo "[$totalNumber]"

       echo "$serialNumber, $GenuineIntel, $Memory, $Storage, $Keyboard, $run_inBeginTime, $run_inEndTime" >> $resultFile

       rm -rf $tempPath

done       