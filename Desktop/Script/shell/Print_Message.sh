#!/bin/sh
set -x
Date=`date +%Y-%m-%d--%H:%M:%S`
SystemSN=`system_profiler SPHardwareDataType | grep "Serial" | sed 's/.*: //'`
Bundle_V=`ls /Phoenix/Tables | grep "PGQ" | awk -F '.tb*' '{print$1}'`
if [ -f /*.dmg ];then 
cd /
CM_Bundle=`ls *.dmg | awk -F '.dmg' '{print$1}'`
fi


echo $SystemSN >> /Volumes/DATA/_UnitsMessage/Runin.txt