#!/bin/sh
#  BoxSNCheck.sh
#  test_v
#
#  Created by Saseny on 12/29/16.
#  Copyright © 2016 Saseny. All rights reserved.

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
    if [ $Status -eq 1 ];then 
       echo "There is [PASS] LOG."
       oneLogPathRoad="/tmp/oneLogCheck/$oneCheckLogName/_PHOENIX_LOGS_PROCESSLOG.PLOG/processlog.plog"
       configLogPath="/tmp/oneLogCheck/$oneCheckLogName/_PHOENIX_CONFIGURATION/Configuration/configExpected.txt"
      else
       echo "There is [FAIL] LOG."
       oneLogPathRoad="/tmp/oneLogCheck/$oneCheckLogName/_PHOENIX_LOGS/Logs/processlog.plog"
       configLogPath="/tmp/oneLogCheck/$oneCheckLogName/_PHOENIX_CONFIGURATION/Configuration/configExpected.txt"
    fi
}    

## Mian ##    

allCheckLog=`ls $logFromPath`
echo "Serial Number,Xenon Box Serial Number,Palladium Box Serial Number" >> $ResultPathroad

for oneCheckLog in $allCheckLog
do 
    mkdir /tmp/oneLogCheck
    cp -rf $logFromPath/$oneCheckLog /tmp/oneLogCheck    
    
    fileFormat=`echo $oneCheckLog | awk -F '.' '{print$NF}'`
    oneCheckLogName=`echo $oneCheckLog | awk -F '.tgz' '{print$1}'`

    cd /tmp/oneLogCheck
    tar -zxvf $oneCheckLog  
    
    CheckLogStatus
    XenonBoxSerialNumber=`cat < $oneLogPathRoad | grep "Found Xenon Test Device" | awk '{print$8}' | sed 's/Serial(//g' | sed 's/)//g' | sort -u`
    echo $XenonBoxSerialNumber >> /tmp/Xenon.txt
#    sort -u -o /tmp/Xenon.txt /tmp/Xenon1.txt
#    rm -rf /tmp/Xenon1.txt
    XenonBoxQTY=`cat -n /tmp/Xenon.txt | tail -1 | awk '{print$1}'`
    case $XenonBoxSerialNumber in 
    *1*)
      XenonBoxOne=`cat < /tmp/Xenon.txt | head -1` 
      XenonResult="$XenonBoxOne"  ;;
    *2*)
      XenonBoxOne=`cat < /tmp/Xenon.txt | head -1`
      XenonBoxTwo=`cat < /tmp/Xenon.txt | sed -n '2p'`
      XenonResult="$XenonBoxOne,$XenonBoxTwo" ;;
    *3*)
      XenonBoxOne=`cat < /tmp/Xenon.txt | head -1`
      XenonBoxTwo=`cat < /tmp/Xenon.txt | sed -n '2p'`
      XenonBoxThree=`cat < /tmp/Xenon.txt | sed -n '3p'`
      XenonResult="$XenonBoxOne,$XenonBoxTwo,$XenonBoxThree" ;; 
    *4*)
      XenonBoxOne=`cat < /tmp/Xenon.txt | head -1`
      XenonBoxTwo=`cat < /tmp/Xenon.txt | sed -n '2p'`
      XenonBoxThree=`cat < /tmp/Xenon.txt | sed -n '3p'`
      XenonBoxFour=`cat < /tmp/Xenon.txt | sed -n '4p'`
      XenonResult="$XenonBoxOne,$XenonBoxTwo,$XenonBoxThree,$XenonBoxFour" ;;
    *5*)
      XenonBoxOne=`cat < /tmp/Xenon.txt | head -1`
      XenonBoxTwo=`cat < /tmp/Xenon.txt | sed -n '2p'`
      XenonBoxThree=`cat < /tmp/Xenon.txt | sed -n '3p'`
      XenonBoxFour=`cat < /tmp/Xenon.txt | sed -n '4p'`
      XenonBoxFive=`cat < /tmp/Xenon.txt | sed -n '5p'`
      XenonResult="$XenonBoxOne,$XenonBoxTwo,$XenonBoxThree,$XenonBoxFour,$XenonBoxFive" ;;  
    *6*)
      XenonBoxOne=`cat < /tmp/Xenon.txt | head -1`
      XenonBoxTwo=`cat < /tmp/Xenon.txt | sed -n '2p'`
      XenonBoxThree=`cat < /tmp/Xenon.txt | sed -n '3p'`
      XenonBoxFour=`cat < /tmp/Xenon.txt | sed -n '4p'`
      XenonBoxFive=`cat < /tmp/Xenon.txt | sed -n '5p'`
      XenonBoxSix=`cat < /tmp/Xenon.txt | sed -n '6p'`
      XenonResult="$XenonBoxOne,$XenonBoxTwo,$XenonBoxThree,$XenonBoxFour,$XenonBoxFive,XenonBoxSix" ;;  
    esac    
    rm -rf /tmp/Xenon.txt
     
     PalladiumBoxSerialNumber=`cat < $oneLogPathRoad | grep "Found Test Box Serial Number:" | awk -F 'Found Test Box Serial Number:' '{print$2}' | awk -F '"' '{print$1}' | sort -u`    
     echo $PalladiumBoxSerialNumber >> /tmp/Palladium.txt
#     sort -u -o /tmp/Palladium.txt /tmp/Palladium1.txt
#     rm -rf /tmp/Palladium1.txt
     PalladiumQTY=`cat -n /tmp/Palladium.txt | tail -1 | awk '{print$1}'`
     case $PalladiumQTY in
     *1*)
       PalladiumBoxOne=`cat < /tmp/Palladium.txt | head -1`
       PalladiumResult="$PalladiumBoxOne" ;;
     *2*)
       PalladiumBoxOne=`cat < /tmp/Palladium.txt | head -1`
       PalladiumBoxTwo=`cat < /tmp/Palladium.txt | sed -n '2p'`
       PalladiumResult="$PalladiumBoxOne,$PalladiumBoxTwo" ;;
     *3*)
       PalladiumBoxOne=`cat < /tmp/Palladium.txt | head -1`
       PalladiumBoxTwo=`cat < /tmp/Palladium.txt | sed -n '2p'`
       PalladiumBoxThree=`cat < /tmp/Palladium.txt | sed -n '3p'`
       PalladiumResult="$PalladiumBoxOne,$PalladiumBoxTwo,$PalladiumBoxThree" ;; 
     *4*)
       PalladiumBoxOne=`cat < /tmp/Palladium.txt | head -1`
       PalladiumBoxTwo=`cat < /tmp/Palladium.txt | sed -n '2p'`
       PalladiumBoxThree=`cat < /tmp/Palladium.txt | sed -n '3p'`
       PalladiumBoxFour=`cat < /tmp/Palladium.txt | sed -n '4p'`
       PalladiumResult="$PalladiumBoxOne,$PalladiumBoxTwo,$PalladiumBoxThree,$PalladiumBoxFour" ;;
     *5*)
       PalladiumBoxOne=`cat < /tmp/Palladium.txt | head -1`
       PalladiumBoxTwo=`cat < /tmp/Palladium.txt | sed -n '2p'`
       PalladiumBoxThree=`cat < /tmp/Palladium.txt | sed -n '3p'`
       PalladiumBoxFour=`cat < /tmp/Palladium.txt | sed -n '4p'`
       PalladiumBoxFive=`cat < /tmp/Palladium.txt | sed -n '5p'`
       PalladiumResult="$PalladiumBoxOne,$PalladiumBoxTwo,$PalladiumBoxThree,$PalladiumBoxFour,PalladiumBoxFive" ;;  
     *6*)
       PalladiumBoxOne=`cat < /tmp/Palladium.txt | head -1`
       PalladiumBoxTwo=`cat < /tmp/Palladium.txt | sed -n '2p'`
       PalladiumBoxThree=`cat < /tmp/Palladium.txt | sed -n '3p'`
       PalladiumBoxFour=`cat < /tmp/Palladium.txt | sed -n '4p'`
       PalladiumBoxFive=`cat < /tmp/Palladium.txt | sed -n '5p'`
       PalladiumBoxSix=`cat < /tmp/Palladium.txt | sed -n '6p'`
       PalladiumResult="$PalladiumBoxOne,$PalladiumBoxTwo,$PalladiumBoxThree,$PalladiumBoxFour,$PalladiumBoxFive,$PalladiumBoxSix" ;;
     *7*)
       PalladiumBoxOne=`cat < /tmp/Palladium.txt | head -1`
       PalladiumBoxTwo=`cat < /tmp/Palladium.txt | sed -n '2p'`
       PalladiumBoxThree=`cat < /tmp/Palladium.txt | sed -n '3p'`
       PalladiumBoxFour=`cat < /tmp/Palladium.txt | sed -n '4p'`
       PalladiumBoxFive=`cat < /tmp/Palladium.txt | sed -n '5p'`
       PalladiumBoxSix=`cat < /tmp/Palladium.txt | sed -n '6p'`
       PalladiumBoxSeven=`cat < /tmp/Palladium.txt | sed -n '7p'`
       PalladiumResult="$PalladiumBoxOne,$PalladiumBoxTwo,$PalladiumBoxThree,$PalladiumBoxFour,$PalladiumBoxFive,$PalladiumBoxSix,$PalladiumBoxSeven" ;;  
     *8*)
       PalladiumBoxOne=`cat < /tmp/Palladium.txt | head -1`
       PalladiumBoxTwo=`cat < /tmp/Palladium.txt | sed -n '2p'`
       PalladiumBoxThree=`cat < /tmp/Palladium.txt | sed -n '3p'`
       PalladiumBoxFour=`cat < /tmp/Palladium.txt | sed -n '4p'`
       PalladiumBoxFive=`cat < /tmp/Palladium.txt | sed -n '5p'`
       PalladiumBoxSix=`cat < /tmp/Palladium.txt | sed -n '6p'`
       PalladiumBoxSeven=`cat < /tmp/Palladium.txt | sed -n '7p'`
       PalladiumBoxEight=`cat < /tmp/Palladium.txt | sed -n '8p'`
       PalladiumResult="$PalladiumBoxOne,$PalladiumBoxTwo,$PalladiumBoxThree,$PalladiumBoxFour,$PalladiumBoxFive,$PalladiumBoxSix,$PalladiumBoxSeven,$PalladiumBoxEight" ;;         
     esac 
     rm -rf /tmp/Palladium.txt        
    SerialNumber=`echo $oneCheckLog | awk -F '_' '{print$1}'` 
       
    echo "$SerialNumber,$XenonResult,$PalladiumResult" >> $ResultPathroad   
    
    
    rm -rf /tmp/oneLogCheck
    
done    