#!/bin/bash

SCRIPT_DIR=`dirname $0`
Date_=`date +%Y%m%d_%H%M%S`
tempPath="$SCRIPT_DIR/tmp"
resultFile="$SCRIPT_DIR/$Date_.csv"

startParameter="CM_Bundle_Verify" 
endParameter="MSD.ntab"
logPathRoad="$SCRIPT_DIR/DOWNLOAD"

# Parameter Set
echo ; echo "--------------------------------------------------------------------------"
[ ! -z $1 ] && logPathRoad="$1" 
  echo "[LogPath: $logPathRoad]" 

[ ! -z $2 ] && startParameter="$2" 
  echo "[startParameter: $startParameter]"

[ ! -z $3 ] && endParameter="$3" 
  echo "[endParameter: $endParameter]"
echo "--------------------------------------------------------------------------" ; echo   

allLog=`ls $logPathRoad`
totalNumber=`ls -n $logPathRoad | grep -c "Dec"`

echo "序列号, 测试次数, CPU, 运行内存, SSD, 键盘国别, 开始时间, 结束时间, 总耗时(Hour)" >> $resultFile

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
       GenuineIntelsource=`cat < $tempPath/$logName/_PHOENIX_CONFIGURATION/Configuration/configExpected.txt | grep "GenuineIntel" | awk -F '=' '{print$3}' | awk -F '&' '{print$1}' | sed 's/"//g'`
       Memory=`cat < $tempPath/$logName/_PHOENIX_CONFIGURATION/Configuration/configExpected.txt | grep "Memory" | awk -F '=' '{print$2}' | awk -F '&' '{print$1}' | sed 's/"//g'`
       Keyboard=`cat < $tempPath/$logName/_PHOENIX_CONFIGURATION/Configuration/configExpected.txt | grep "Keyboard" | tail -1 | awk -F '=' '{print$3}' | awk -F '&' '{print$1}' | sed 's/"//g'`

       run_inBeginTime=`cat < $tempPath/$logName/_PHOENIX_LOGS_PROCESSLOG.PLOG/processlog.plog | grep "$startParameter" | head -1 | awk -F ',' '{print$2}' | sed 's/.*=//' | sed 's/"//g'`
       run_inEndTime=`cat < $tempPath/$logName/_PHOENIX_LOGS_PROCESSLOG.PLOG/processlog.plog | grep "$endParameter" | tail -1 | awk -F ',' '{print$2}' | sed 's/.*=//' | sed 's/"//g'`
       
       A=1000
       GenuineIntel=`echo "scale=1;$TimeUsed/$A" |bc`
       
       let totalNumber-=1
       echo "[$totalNumber]"
       ## Time Calculate
       StartTimeSample=`date -j -f date -j -f "%Y/%m/%d %T" "$run_inBeginTime" +"%s"`
       EndTimeSample=`date -j -f date -j -f "%Y/%m/%d %T" "$run_inEndTime" +"%s"`
       TimeUsed=`expr ${EndTimeSample} - ${StartTimeSample}`
       B=3600
       timeleft=`echo "scale=2;$TimeUsed/$B" |bc`
       
       testTimes=`ls $logPathRoad | grep -c "$serialNumber"`
       outPutMessage="$serialNumber, $testTimes, $GenuineIntel, $Memory, $Storage, $Keyboard, $run_inBeginTime, $run_inEndTime, $timeleft"        
       
       if [ $testTimes -gt 1 ];then
           echo 1 >> $SCRIPT_DIR/count.log
           count=`cat < $SCRIPT_DIR/count.log | grep -c "1"`          
           if [ $count -eq $testTimes ];then                          
             echo $outPutMessage >> $resultFile
             rm -rf $SCRIPT_DIR/count.log
           fi     
         else              
           echo $outPutMessage >> $resultFile 
       fi    

       rm -rf $tempPath

done       