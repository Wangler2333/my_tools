#!/bin/sh

sleep 1

expectFW="901"
expectMF="SMP"

BAFW=`system_profiler SPPowerDataType | grep "Firmware Version" | head -1 | sed 's/.*: //'`

BAMF=`system_profiler SPPowerDataType | grep "Manufacturer" | head -1 | sed 's/.*: //'`

if [ $BAFW == $expectFW ] && [ $BAMF == $expectMF ];then
	echo "Correct Battery FW !!!"
	exit 0
else
	echo "Wrong Battery FW !!!"
	exit 0
fi