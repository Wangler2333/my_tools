#!/bin/sh

SCRIPT_DIR=`dirname $0`
Date=`date +%Y%m%d_%H%M%S`
logPathroad=$1
resultPath="$SCRIPT_DIR/$Date.csv"


allLog=`ls $logPathroad`

echo "Serial Number,SSD Size,BootRom,timeleft(min)" >> $resultPath

for onelog in $allLog
do 
   mkdir -p $SCRIPT_DIR/tmp
   cp -rf $logPathroad/$onelog $SCRIPT_DIR/tmp
   cd $SCRIPT_DIR/tmp
   
   if [ `echo $onelog | grep -c "tgz"` -eq 0 ];then
      gunzip $onelog
      logName=`echo $onelog | awk -F '.gz' '{print$1}'`
    
   
   SerialNumber=`echo $onelog | awk -F '_' '{print$1}'`

   BootRom=`cat < $SCRIPT_DIR/tmp/$logName | grep "(bodega-info) Name:" | sed 's/.*: //' | head -1`
   #IFS='''

   SSD_Size=`cat < $SCRIPT_DIR/tmp/$logName | grep "SSD_CAPACITY" | sed 's/.*= //' | head -1`

   startTime=`cat < $SCRIPT_DIR/tmp/$logName | head -1 | awk '{print$1,$2}'`
   endTime=`cat < $SCRIPT_DIR/tmp/$logName | tail -1 | awk '{print$1,$2}'`

StartTimeSample=`date -j -f date -j -f "%Y-%m-%d %T" "$startTime" +"%s"`
EndTimeSample=`date -j -f date -j -f "%Y-%m-%d %T" "$endTime" +"%s"`
TimeUsed=`expr ${EndTimeSample} - ${StartTimeSample}`
B=60
timeleft=`echo "scale=2;$TimeUsed/$B" |bc`

echo "$SerialNumber,$SSD_Size,$BootRom,$timeleft" >> $resultPath

rm -rf $SCRIPT_DIR/tmp

 #else
      #tar -zxvf $SCRIPT_DIR/tmp/$oneLog
      #rm -rf $SCRIPT_DIR/tmp/$oneLog 
fi   

done
