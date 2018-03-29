#!/bin/sh

SerialNumber=`system_profiler SPHardwareDataType | grep "Serial" | sed 's/.*: //'`
Name=$SerialNumber"-ypc2"
Time=`date +%y-%m-%d_%H:%M:%S`

mkdir /Users/bundle/Desktop/SMC

ypc2 > /tmp/ypc2.txt

Key=`cat < /tmp/ypc2.txt | awk '{print$2}'`

echo $Time >> /Users/bundle/Desktop/SMC/$Name.log

for B in $Key
do 
Volue=`ypc2 -drk $B`
echo $B:$Volue >> /Users/bundle/Desktop/SMC/$Name.log
done

sleep 3
rm -rf /tmp/ypc2.txt

## | sed 's/\..*//'
