#!/bin/sh

#  BoxSNCheck1.sh
#  test_v
#
#  Created by Saseny on 12/29/16.
#  Copyright © 2016 Saseny. All rights reserved.
#  Base on BoxSNCheck.sh changed output format.

SCRIPT_DIR=`dirname $0`
BASENAME=`basename $0`
Date=`date +%Y%m%d_%H%M%S`

ResultPathroad="$SCRIPT_DIR/$Date.csv"

if [ -z $1 ];then
    logFromPath="/Users/saseny/Desktop/LOG"
  else
    logFromPath=$1 
fi

CheckLogStatus()
{
    Status=`echo $oneCheckLog | grep -c "PASS"`
    let A+=1
    if [ $Status -eq 1 ];then 
       echo "[$A] There is [PASS] LOG."
       oneLogPathRoad="/tmp/oneLogCheck/$oneCheckLogName/_PHOENIX_LOGS_PROCESSLOG.PLOG/processlog.plog"
       configLogPath="/tmp/oneLogCheck/$oneCheckLogName/_PHOENIX_CONFIGURATION/Configuration/configExpected.txt"
      else
       echo "[$A] There is [FAIL] LOG."
       oneLogPathRoad="/tmp/oneLogCheck/$oneCheckLogName/_PHOENIX_LOGS/Logs/processlog.plog"
       configLogPath="/tmp/oneLogCheck/$oneCheckLogName/_PHOENIX_CONFIGURATION/Configuration/configExpected.txt"
    fi
}    

## Mian ##    

allCheckLog=`ls $logFromPath`
#echo "Serial Number,Xenon Box Serial Number,Palladium Box Serial Number" >> $ResultPathroad
A=0

for oneCheckLog in $allCheckLog
do 
    mkdir /tmp/oneLogCheck
    cp -rf $logFromPath/$oneCheckLog /tmp/oneLogCheck  &>/dev/null   
    
    fileFormat=`echo $oneCheckLog | awk -F '.' '{print$NF}'`
    case $fileFormat in 
    *tgz*)
       oneCheckLogName=`echo $oneCheckLog | awk -F '.tgz' '{print$1}'`
       cd /tmp/oneLogCheck
       tar -zxvf $oneCheckLog  &>/dev/null   ;;
    *tar*)
       oneCheckLogName=`echo $oneCheckLog | awk -F '.tar' '{print$1}'`
       cd /tmp/oneLogCheck
       tar xvf $oneCheckLog  &>/dev/null   ;; 
    *)
       echo "Wrong File Format!!!"
    esac               
    
    CheckLogStatus
    XenonBoxSerialNumber=`cat < $oneLogPathRoad | grep "Found Xenon Test Device" | awk '{print$8}' | sed 's/Serial(//g' | sed 's/)//g' | sort -u | grep -c "FA*"`
    case $XenonBoxSerialNumber in 
    *1*)
      XenonBoxOne=`cat < $oneLogPathRoad | grep "Found Xenon Test Device" | awk '{print$8}' | sed 's/Serial(//g' | sed 's/)//g' | sort -u | head -1` 
      XenonResult="$XenonBoxOne"  ;;
    *2*)
      XenonBoxOne=`cat < $oneLogPathRoad | grep "Found Xenon Test Device" | awk '{print$8}' | sed 's/Serial(//g' | sed 's/)//g' | sort -u | head -1`
      XenonBoxTwo=`cat < $oneLogPathRoad | grep "Found Xenon Test Device" | awk '{print$8}' | sed 's/Serial(//g' | sed 's/)//g' | sort -u | sed -n '2p'`
      XenonResult="$XenonBoxOne,$XenonBoxTwo" ;;
    *3*)
      XenonBoxOne=`cat < $oneLogPathRoad | grep "Found Xenon Test Device" | awk '{print$8}' | sed 's/Serial(//g' | sed 's/)//g' | sort -u | head -1`
      XenonBoxTwo=`cat < $oneLogPathRoad | grep "Found Xenon Test Device" | awk '{print$8}' | sed 's/Serial(//g' | sed 's/)//g' | sort -u | sed -n '2p'`
      XenonBoxThree=`cat < $oneLogPathRoad | grep "Found Xenon Test Device" | awk '{print$8}' | sed 's/Serial(//g' | sed 's/)//g' | sort -u | sed -n '3p'`
      XenonResult="$XenonBoxOne,$XenonBoxTwo,$XenonBoxThree" ;; 
    *4*)
      XenonBoxOne=`cat < $oneLogPathRoad | grep "Found Xenon Test Device" | awk '{print$8}' | sed 's/Serial(//g' | sed 's/)//g' | sort -u | head -1`
      XenonBoxTwo=`cat < $oneLogPathRoad | grep "Found Xenon Test Device" | awk '{print$8}' | sed 's/Serial(//g' | sed 's/)//g' | sort -u | sed -n '2p'`
      XenonBoxThree=`cat < $oneLogPathRoad | grep "Found Xenon Test Device" | awk '{print$8}' | sed 's/Serial(//g' | sed 's/)//g' | sort -u | sed -n '3p'`
      XenonBoxFour=`cat < $oneLogPathRoad | grep "Found Xenon Test Device" | awk '{print$8}' | sed 's/Serial(//g' | sed 's/)//g' | sort -u | sed -n '4p'`
      XenonResult="$XenonBoxOne,$XenonBoxTwo,$XenonBoxThree,$XenonBoxFour" ;;
    *5*)
      XenonBoxOne=`cat < $oneLogPathRoad | grep "Found Xenon Test Device" | awk '{print$8}' | sed 's/Serial(//g' | sed 's/)//g' | sort -u | head -1`
      XenonBoxTwo=`cat < $oneLogPathRoad | grep "Found Xenon Test Device" | awk '{print$8}' | sed 's/Serial(//g' | sed 's/)//g' | sort -u | sed -n '2p'`
      XenonBoxThree=`cat < $oneLogPathRoad | grep "Found Xenon Test Device" | awk '{print$8}' | sed 's/Serial(//g' | sed 's/)//g' | sort -u | sed -n '3p'`
      XenonBoxFour=`cat < $oneLogPathRoad | grep "Found Xenon Test Device" | awk '{print$8}' | sed 's/Serial(//g' | sed 's/)//g' | sort -u | sed -n '4p'`
      XenonBoxFive=`cat < $oneLogPathRoad | grep "Found Xenon Test Device" | awk '{print$8}' | sed 's/Serial(//g' | sed 's/)//g' | sort -u | sed -n '5p'`
      XenonResult="$XenonBoxOne,$XenonBoxTwo,$XenonBoxThree,$XenonBoxFour,$XenonBoxFive" ;;  
    *6*)
      XenonBoxOne=`cat < $oneLogPathRoad | grep "Found Xenon Test Device" | awk '{print$8}' | sed 's/Serial(//g' | sed 's/)//g' | sort -u | head -1`
      XenonBoxTwo=`cat < $oneLogPathRoad | grep "Found Xenon Test Device" | awk '{print$8}' | sed 's/Serial(//g' | sed 's/)//g' | sort -u | sed -n '2p'`
      XenonBoxThree=`cat < $oneLogPathRoad | grep "Found Xenon Test Device" | awk '{print$8}' | sed 's/Serial(//g' | sed 's/)//g' | sort -u | sed -n '3p'`
      XenonBoxFour=`cat < $oneLogPathRoad | grep "Found Xenon Test Device" | awk '{print$8}' | sed 's/Serial(//g' | sed 's/)//g' | sort -u | sed -n '4p'`
      XenonBoxFive=`cat < $oneLogPathRoad | grep "Found Xenon Test Device" | awk '{print$8}' | sed 's/Serial(//g' | sed 's/)//g' | sort -u | sed -n '5p'`
      XenonBoxSix=`cat < $oneLogPathRoad | grep "Found Xenon Test Device" | awk '{print$8}' | sed 's/Serial(//g' | sed 's/)//g' | sort -u | sed -n '6p'`
      XenonResult="$XenonBoxOne,$XenonBoxTwo,$XenonBoxThree,$XenonBoxFour,$XenonBoxFive,XenonBoxSix" ;;  
    esac    
    rm -rf /tmp/Xenon.txt  &>/dev/null
     
     PalladiumBoxSerialNumber=`cat < $oneLogPathRoad | grep "Found Test Box Serial Number:" | awk -F 'Found Test Box Serial Number:' '{print$2}' | awk -F '"' '{print$1}' | sort -u | grep -c "FA*"`    
     case $PalladiumBoxSerialNumber in
     *1*)
       PalladiumBoxOne=`cat < $oneLogPathRoad | grep "Found Test Box Serial Number:" | awk -F 'Found Test Box Serial Number:' '{print$2}' | awk -F '"' '{print$1}' | sort -u | head -1`
       PalladiumResult="$PalladiumBoxOne" ;;
     *2*)
       PalladiumBoxOne=`cat < $oneLogPathRoad | grep "Found Test Box Serial Number:" | awk -F 'Found Test Box Serial Number:' '{print$2}' | awk -F '"' '{print$1}' | sort -u | head -1`
       PalladiumBoxTwo=`cat < $oneLogPathRoad | grep "Found Test Box Serial Number:" | awk -F 'Found Test Box Serial Number:' '{print$2}' | awk -F '"' '{print$1}' | sort -u | sed -n '2p'`
       PalladiumResult="$PalladiumBoxOne,$PalladiumBoxTwo" ;;
     *3*)
       PalladiumBoxOne=`cat < $oneLogPathRoad | grep "Found Test Box Serial Number:" | awk -F 'Found Test Box Serial Number:' '{print$2}' | awk -F '"' '{print$1}' | sort -u | head -1`
       PalladiumBoxTwo=`cat < $oneLogPathRoad | grep "Found Test Box Serial Number:" | awk -F 'Found Test Box Serial Number:' '{print$2}' | awk -F '"' '{print$1}' | sort -u | sed -n '2p'`
       PalladiumBoxThree=`cat < $oneLogPathRoad | grep "Found Test Box Serial Number:" | awk -F 'Found Test Box Serial Number:' '{print$2}' | awk -F '"' '{print$1}' | sort -u | sed -n '3p'`
       PalladiumResult="$PalladiumBoxOne,$PalladiumBoxTwo,$PalladiumBoxThree" ;; 
     *4*)
       PalladiumBoxOne=`cat < $oneLogPathRoad | grep "Found Test Box Serial Number:" | awk -F 'Found Test Box Serial Number:' '{print$2}' | awk -F '"' '{print$1}' | sort -u | head -1`
       PalladiumBoxTwo=`cat < $oneLogPathRoad | grep "Found Test Box Serial Number:" | awk -F 'Found Test Box Serial Number:' '{print$2}' | awk -F '"' '{print$1}' | sort -u | sed -n '2p'`
       PalladiumBoxThree=`cat < $oneLogPathRoad | grep "Found Test Box Serial Number:" | awk -F 'Found Test Box Serial Number:' '{print$2}' | awk -F '"' '{print$1}' | sort -u | sed -n '3p'`
       PalladiumBoxFour=`cat < $oneLogPathRoad | grep "Found Test Box Serial Number:" | awk -F 'Found Test Box Serial Number:' '{print$2}' | awk -F '"' '{print$1}' | sort -u | sed -n '4p'`
       PalladiumResult="$PalladiumBoxOne,$PalladiumBoxTwo,$PalladiumBoxThree,$PalladiumBoxFour" ;;
     *5*)
       PalladiumBoxOne=`cat < $oneLogPathRoad | grep "Found Test Box Serial Number:" | awk -F 'Found Test Box Serial Number:' '{print$2}' | awk -F '"' '{print$1}' | sort -u | head -1`
       PalladiumBoxTwo=`cat < $oneLogPathRoad | grep "Found Test Box Serial Number:" | awk -F 'Found Test Box Serial Number:' '{print$2}' | awk -F '"' '{print$1}' | sort -u | sed -n '2p'`
       PalladiumBoxThree=`cat < $oneLogPathRoad | grep "Found Test Box Serial Number:" | awk -F 'Found Test Box Serial Number:' '{print$2}' | awk -F '"' '{print$1}' | sort -u | sed -n '3p'`
       PalladiumBoxThree=`cat < $oneLogPathRoad | grep "Found Test Box Serial Number:" | awk -F 'Found Test Box Serial Number:' '{print$2}' | awk -F '"' '{print$1}' | sort -u | sed -n '4p'`
       PalladiumBoxFive=`cat < $oneLogPathRoad | grep "Found Test Box Serial Number:" | awk -F 'Found Test Box Serial Number:' '{print$2}' | awk -F '"' '{print$1}' | sort -u | sed -n '5p'`
       PalladiumResult="$PalladiumBoxOne,$PalladiumBoxTwo,$PalladiumBoxThree,$PalladiumBoxFour,$PalladiumBoxFive" ;;  
     *6*)
       PalladiumBoxOne=`cat < $oneLogPathRoad | grep "Found Test Box Serial Number:" | awk -F 'Found Test Box Serial Number:' '{print$2}' | awk -F '"' '{print$1}' | sort -u | head -1`
       PalladiumBoxTwo=`cat < $oneLogPathRoad | grep "Found Test Box Serial Number:" | awk -F 'Found Test Box Serial Number:' '{print$2}' | awk -F '"' '{print$1}' | sort -u | sed -n '2p'`
       PalladiumBoxThree=`cat < $oneLogPathRoad | grep "Found Test Box Serial Number:" | awk -F 'Found Test Box Serial Number:' '{print$2}' | awk -F '"' '{print$1}' | sort -u | sed -n '3p'`
       PalladiumBoxThree=`cat < $oneLogPathRoad | grep "Found Test Box Serial Number:" | awk -F 'Found Test Box Serial Number:' '{print$2}' | awk -F '"' '{print$1}' | sort -u | sed -n '4p'`
       PalladiumBoxFive=`cat < $oneLogPathRoad | grep "Found Test Box Serial Number:" | awk -F 'Found Test Box Serial Number:' '{print$2}' | awk -F '"' '{print$1}' | sort -u | sed -n '5p'`
       PalladiumBoxFive=`cat < $oneLogPathRoad | grep "Found Test Box Serial Number:" | awk -F 'Found Test Box Serial Number:' '{print$2}' | awk -F '"' '{print$1}' | sort -u | sed -n '6p'`
       PalladiumResult="$PalladiumBoxOne,$PalladiumBoxTwo,$PalladiumBoxThree,$PalladiumBoxFour,$PalladiumBoxFive,$PalladiumBoxSix" ;;
     *7*)
       PalladiumBoxOne=`cat < $oneLogPathRoad | grep "Found Test Box Serial Number:" | awk -F 'Found Test Box Serial Number:' '{print$2}' | awk -F '"' '{print$1}' | sort -u | head -1`
       PalladiumBoxTwo=`cat < $oneLogPathRoad | grep "Found Test Box Serial Number:" | awk -F 'Found Test Box Serial Number:' '{print$2}' | awk -F '"' '{print$1}' | sort -u | sed -n '2p'`
       PalladiumBoxThree=`cat < $oneLogPathRoad | grep "Found Test Box Serial Number:" | awk -F 'Found Test Box Serial Number:' '{print$2}' | awk -F '"' '{print$1}' | sort -u | sed -n '3p'`
       PalladiumBoxThree=`cat < $oneLogPathRoad | grep "Found Test Box Serial Number:" | awk -F 'Found Test Box Serial Number:' '{print$2}' | awk -F '"' '{print$1}' | sort -u | sed -n '4p'`
       PalladiumBoxFive=`cat < $oneLogPathRoad | grep "Found Test Box Serial Number:" | awk -F 'Found Test Box Serial Number:' '{print$2}' | awk -F '"' '{print$1}' | sort -u | sed -n '5p'`
       PalladiumBoxFive=`cat < $oneLogPathRoad | grep "Found Test Box Serial Number:" | awk -F 'Found Test Box Serial Number:' '{print$2}' | awk -F '"' '{print$1}' | sort -u | sed -n '6p'`
       PalladiumBoxSeven=`cat < $oneLogPathRoad | grep "Found Test Box Serial Number:" | awk -F 'Found Test Box Serial Number:' '{print$2}' | awk -F '"' '{print$1}' | sort -u | sed -n '7p'`
       PalladiumResult="$PalladiumBoxOne,$PalladiumBoxTwo,$PalladiumBoxThree,$PalladiumBoxFour,$PalladiumBoxFive,$PalladiumBoxSix,$PalladiumBoxSeven" ;;  
     *8*)
       PalladiumBoxOne=`cat < $oneLogPathRoad | grep "Found Test Box Serial Number:" | awk -F 'Found Test Box Serial Number:' '{print$2}' | awk -F '"' '{print$1}' | sort -u | head -1`
       PalladiumBoxTwo=`cat < $oneLogPathRoad | grep "Found Test Box Serial Number:" | awk -F 'Found Test Box Serial Number:' '{print$2}' | awk -F '"' '{print$1}' | sort -u | sed -n '2p'`
       PalladiumBoxThree=`cat < $oneLogPathRoad | grep "Found Test Box Serial Number:" | awk -F 'Found Test Box Serial Number:' '{print$2}' | awk -F '"' '{print$1}' | sort -u | sed -n '3p'`
       PalladiumBoxThree=`cat < $oneLogPathRoad | grep "Found Test Box Serial Number:" | awk -F 'Found Test Box Serial Number:' '{print$2}' | awk -F '"' '{print$1}' | sort -u | sed -n '4p'`
       PalladiumBoxFive=`cat < $oneLogPathRoad | grep "Found Test Box Serial Number:" | awk -F 'Found Test Box Serial Number:' '{print$2}' | awk -F '"' '{print$1}' | sort -u | sed -n '5p'`
       PalladiumBoxFive=`cat < $oneLogPathRoad | grep "Found Test Box Serial Number:" | awk -F 'Found Test Box Serial Number:' '{print$2}' | awk -F '"' '{print$1}' | sort -u | sed -n '6p'`
       PalladiumBoxSeven=`cat < $oneLogPathRoad | grep "Found Test Box Serial Number:" | awk -F 'Found Test Box Serial Number:' '{print$2}' | awk -F '"' '{print$1}' | sort -u | sed -n '7p'`
       PalladiumBoxSeven=`cat < $oneLogPathRoad | grep "Found Test Box Serial Number:" | awk -F 'Found Test Box Serial Number:' '{print$2}' | awk -F '"' '{print$1}' | sort -u | sed -n '8p'`
       PalladiumResult="$PalladiumBoxOne,$PalladiumBoxTwo,$PalladiumBoxThree,$PalladiumBoxFour,$PalladiumBoxFive,$PalladiumBoxSix,$PalladiumBoxSeven,$PalladiumBoxEight" ;;         
     esac 
     rm -rf /tmp/Palladium.txt  &>/dev/null        
    SerialNumber=`echo $oneCheckLog | awk -F '_' '{print$1}'` 
       
    echo "$SerialNumber,XenonBox,$XenonResult,PalladiumBox,$PalladiumResult" >> $ResultPathroad   
    
    
    rm -rf /tmp/oneLogCheck
    
done    