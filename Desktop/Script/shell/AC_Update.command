#!/bin/sh

ACFW=`system_profiler SPPowerDataType | grep "Firmware Version:" | sed 's/.*: //' | tail -1`

if [ "$ACFW" != "1090011" ];then
	echo "Old FW Adaptor !"
	cp -rf /Volumes/Phoenix/ACFW/b280up_01090011 /
	sleep 1
	sudo /b280up_01090011
else
	echo "Latest FW !"
fi