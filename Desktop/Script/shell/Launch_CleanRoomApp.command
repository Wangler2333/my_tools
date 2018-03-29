#!/bin/sh

stat=`ps aux |grep '/Applications/PhoenixCE' |grep "Content" |grep -c '/MacOS/PhoenixCE'`
while [ 1 ]; do
if [ $stat -eq 1 ];then
echo "Phoenix is running"
sleep 1
else if [ $stat -eq 0 ];then
echo "Phoenix was Stopped"
sleep 3
open /TE_Support/Tools/Yellow/CleanRoomSelection.app
break 1
fi
fi
stat=`ps aux |grep '/Applications/PhoenixCE' |grep "Content" |grep -c '/MacOS/PhoenixCE'`
done

