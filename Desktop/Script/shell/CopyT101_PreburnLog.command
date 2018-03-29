#!/bin/sh

echo "Copy Preburn T101 Log.."

rm -Rf /Phoenix/Logs/T101Cal_PreburnLog

if [ ! -f /Phoenix/Logs/T101Cal_PreburnLog ];then
	mkdir /Phoenix/Logs/T101Cal_PreburnLog
fi

cp -R /private/var/root/Library/Application\ Support/T101Cal/* /Phoenix/Logs/T101Cal_PreburnLog

sleep 1

TimeStamp=`date +%Y_%m_%d_%H_%M_%S`

mv /private/var/root/Library/Application\ Support/T101Cal /private/var/root/Library/Application\ Support/T101Cal_PreburnLog_"$TimeStamp"
		
exit 0


