#!/bin/sh
set -x
cd /
Download_CM=`ls *.dmg | awk -F '.dmg' '{print$1}'`
Scan_CM=`cat /Phoenix/Configuration/bundlelist.txt  | grep "694" | awk -F '<*>' '{print$2}' | awk -F '<' '{print$1}'`
Need_CM=`cat /Phoenix/Tools/Settings/CMImageList.plist | grep "694" | awk -F '<*>' '{print$2}' | awk -F '.' '{print$1}'`

if [ ! -f /*.dmg ];then 
echo " No CM Bundle "
exit 1
fi 

if [ $Download_CM == $Need_CM ];then 
echo " CM : Download Matched Need ! "
     if [ $Scan_CM == $Need_CM ];then 
         echo " CM : Scan Matched Need ! "
         exit 0
     fi 
     echo " CM : Scan Mismatched Need ! Pls Check Scan CM Number . "   
     exit 1
fi
echo " CM : Download Mismatched Need ! Pls Check CM Bundle Download . "
exit 1
