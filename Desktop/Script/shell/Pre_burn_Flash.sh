#!/bin/sh

Date=`date +%Y%m%d_%H%M%S`
SCRIPT_DIR=`dirname $0`

tempPath="$SCRIPT_DIR/tmp"
resultFile="$SCRIPT_DIR/$Date_.csv"

logPathRoad="$SCRIPT_DIR/DOWNLOAD"

mkdir $SCRIPT_DIR/36_0B1


for oneLog in $allLog
do     

       mkdir -p $tempPath
       cp -rf $logPathRoad/$oneLog $tempPath
       cd $tempPath
       tar -zxvf $tempPath/$oneLog 
       rm -rf $tempPath/$oneLog 
       
       serialNumber=`echo $oneLog | awk -F '_' '{print$1}'`
       logName=`echo $oneLog | awk -F '.tgz' '{print$1}'`  
       
       if [ `cat < $tempPath/$logName/_PHOENIX_LOGS_PROCESSLOG.PLOG/processlog.plog | grep -c "PGQ_Ramp_5-11.29.0B1"` -ne 0 ];then
           if [ `cat < $tempPath/$logName/_PHOENIX_LOGS_PROCESSLOG.PLOG/processlog.plog | grep -c "PGQ_Ramp_5-11.36.0B1"` -eq 1 ];then 
              BeginTime=`cat < $tempPath/$logName/_PHOENIX_LOGS_PROCESSLOG.PLOG/processlog.plog | sed -n '2p' | awk -F ',' '{print$2}' | sed 's/"//g' | sed 's/.*=//'`
              FlashEndTime=`cat < $tempPath/$logName/_PHOENIX_LOGS_PROCESSLOG.PLOG/processlog.plog | grep "NET_Check.sh" | head -1 | awk -F ',' '{print$2}' | sed 's/"//g' | sed 's/.*=//'`
              BeginTimez=`date -j -f date -j -f "%Y/%m/%d %T" "$BeginTime" +"%s"`   
              FlashEndTimez=`date -j -f date -j -f "%Y/%m/%d %T" "$FlashEndTime" +"%s"`
              FlashUseTime=`expr ${FlashEndTimez} - ${BeginTimez}`
              B=60
              Flashtimeleft=`echo "scale=2;$FlashUseTime/$B" |bc`        ######
              
              cp -rf $logPathRoad/$serialNumbers* $SCRIPT_DIR/36_0B1
              
              
              
              
              
              
              
              
              echo "$serialNumber,$Flashtimeleft
              
              
              
            fi
        fi
done              