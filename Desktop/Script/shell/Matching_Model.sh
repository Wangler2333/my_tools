#!/bin/sh

set -x


SN_Source="/Users/bundle/Desktop/LL.txt"
Model_Source="/Volumes/DATA/_UnitsMessage/ModelMessage.txt"
Output=`echo $0 | awk -F 'Matching_Model.sh' '{print$1}'`

ABC=`cat < $SN_Source`


for A in $ABC
do 
  EECode=`echo $A | tail -c 5`
  Model=`cat < $Model_Source | grep "$EECode" | awk '{print$1}'`
  SN=`cat < $SN_Source | grep "$EECode"`
  WIP="$SN"+"$Model"
  echo $WIP >> $Output/New.txt
done  
  
  
