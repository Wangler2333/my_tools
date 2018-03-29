#!/bin/sh

sleep 5

expectFW="1090011"

ACFW=`system_profiler SPPowerDataType | grep "Firmware Version" | tail -1 | sed 's/.*: //'`

if [ $ACFW != $expectFW ];then
	echo "Wrong Adaptor FW or No Adaptor plugged !!!"
	exit 1
else
	echo "Correct Adaptor FW !!!"
	exit 0
fi