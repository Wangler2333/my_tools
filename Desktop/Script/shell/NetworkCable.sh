#!/bin/sh

Network=`system_profiler SPUSBDataType | grep -c "Apple USB Ethernet Adapter"`
while [ $Network -eq 1 ]
do 
  echo " Pls unplug Network Cable "
  sleep 1
  Network=`system_profiler SPUSBDataType | grep -c "Apple USB Ethernet Adapter"`
done  