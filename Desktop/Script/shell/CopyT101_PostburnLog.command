#!/bin/sh

echo "Copy Postburn T101 Log.."

rm -Rf /Phoenix/Logs/T101Cal_PostburnLog

if [ ! -f /Phoenix/Logs/T101Cal_PostburnLog ];then
	mkdir /Phoenix/Logs/T101Cal_PostburnLog
fi

cp -R /private/var/root/Library/Application\ Support/T101Cal/* /Phoenix/Logs/T101Cal_PostburnLog

sleep 1

TimeStamp=`date +%Y_%m_%d_%H_%M_%S`

mv /private/var/root/Library/Application\ Support/T101Cal /private/var/root/Library/Application\ Support/T101Cal_PostburnLog_"$TimeStamp"
		
exit 0


