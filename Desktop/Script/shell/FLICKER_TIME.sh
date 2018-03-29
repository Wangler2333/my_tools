#!/bin/sh

SCRIPT_DIR=`dirname $0`
Date=`date +%Y%m%d_%H%M%S`
logPath=$1
resultPath="$SCRIPT_DIR/$Date.csv"
tmpPath="$SCRIPT_DIR/tmp"

echo "Serial Number,TotalTime,INITIALIZING_IP,CB not PASS,Over Allowed Relative Fail Count,Over Allowed Relative Fail Count,Write CB to Incomplete,DUT_POSITION_CHECK,GREY128_PATTERN,PSR128_MODE_ON,MEASURE_CA310,PSR128_MODE_OFF,GREY75_PATTERN,PSR75_MODE_ON,MEASURE_CA310,PSR75_MODE_OFF,FAILURE_MESSAGE" >> $resultPath

allLog=`ls $logPath`

for oneLog in $allLog
do  
    mkdir -p $tmpPath/tmep
    cp -rf $logPath/$oneLog $tmpPath/tmep
    cd $tmpPath/tmep
    unzip $oneLog
    rm -rf $tmpPath/tmep/$oneLog
    
    ## Parameter read
    SerialNumber=`echo $oneLog | awk -F '_' '{print$1}'`
    
    FAILURE_MESSAGE=`cat < $tmpPath/tmep/$SerialNumber.log | grep "FAILURE_MESSAGE" | sed -n '/NA/!p' | sed 's/.*://'`
    
    
    CycleName="$SerialNumber""_CycleTime.txt" 
      
    timeOne=`cat < $tmpPath/tmep/$CycleName | sed -n '1p' | awk '{print$NF}'`  
    timeTwo=`cat < $tmpPath/tmep/$CycleName | sed -n '3p' | awk '{print$NF}'`
    timeThree=`cat < $tmpPath/tmep/$CycleName | sed -n '5p' | awk '{print$NF}'`
    timeFour=`cat < $tmpPath/tmep/$CycleName | sed -n '7p' | awk '{print$NF}'`
    timeFive=`cat < $tmpPath/tmep/$CycleName | sed -n '9p' | awk '{print$NF}'`
    timeSix=`cat < $tmpPath/tmep/$CycleName | sed -n '11p' | awk '{print$NF}'`
    timeSeven=`cat < $tmpPath/tmep/$CycleName | sed -n '13p' | awk '{print$NF}'`
    timeEight=`cat < $tmpPath/tmep/$CycleName | sed -n '15p' | awk '{print$NF}'`
    timeNine=`cat < $tmpPath/tmep/$CycleName | sed -n '17p' | awk '{print$NF}'`
    timeTen=`cat < $tmpPath/tmep/$CycleName | sed -n '19p' | awk '{print$NF}'`
    timeEleven=`cat < $tmpPath/tmep/$CycleName | sed -n '21p' | awk '{print$NF}'`
    timeTweleve=`cat < $tmpPath/tmep/$CycleName | sed -n '23p' | awk '{print$NF}'`
    timeThirteen=`cat < $tmpPath/tmep/$CycleName | sed -n '25p' | awk '{print$NF}'`
    timeFourteen=`cat < $tmpPath/tmep/$CycleName | sed -n '27p' | awk '{print$NF}'`
    
    totalTime=`echo "scale=6;$timeOne+$timeTwo+$timeThree+$timeFour+$timeFive+$timeSix+$timeSeven+$timeEight+$timeNine+$timeTen+$timeEleven+$timeTweleve+$timeThirteen+$timeFourteen" |bc`
    resultMessage="$SerialNumber,$totalTime,$timeOne,$timeTwo,$timeThree,$timeFour,$timeFive,$timeSix,$timeSeven,$timeEight,$timeNine,$timeTen,$timeEleven,$timeTweleve,$timeThirteen,$timeFourteen,$FAILURE_MESSAGE" 
    echo $resultMessage >> $resultPath
    
    rm -rf $tmpPath/tmep
    
done  

rm -rf $tmpPath