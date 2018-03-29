#!/bin/sh

Dir=`dirname $0`
starTime=`date +%s`
Password=$4

$Dir/earse_Lobo.sh

expect -c "set timeout 2;spawn $Dir/DownloadCommand.sh $1 $2 $3; expect -re \".*password*\";send \"$Password\r\";expect -re \"$\";interact"

endTime=`date +%s`
useTimeSample=`expr ${endTime} - ${starTime}`
B=60
timeleft=`echo "scale=2;$useTimeSample/$B" |bc` ; echo 
echo "\033[34m [UsedTime: $timeleft min] \033[30m"