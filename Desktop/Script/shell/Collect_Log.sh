#!/bin/sh
set -x
SystemSN=`system_profiler SPHardwareDataType | grep "Serial" | sed 's/.*: //'`
Date=`date +%Y-%m-%d--%H:%M:%S`
if [ -z $SystemSN ];then 
SystemSN=`cat < /Phoenix/Logs/state.txt | grep "WIP" | awk '{print$6}' | awk -F '+' '{print$1}'`
fi 
SNMessage=`cat < /Volumes/DATA/_UnitsMessage/SN.txt | awk -F ';' '{print$2}'`
Bundle_V=`ls /Phoenix/Tables | grep "PGQ" | awk -F '.tb*' '{print$1}'`
A="#"
B="\n"
cd /Volumes/DATA/_Script
chmod +x Mkdir.sh
/Volumes/DATA/_Script/Mkdir.sh
for SN in $SNMessage ; do 
if [ $SN == $SystemSN ];then 
UN=`cat < /Volumes/DATA/_UnitsMessage/SN.txt | grep "$SN" | awk -F ';' '{print$1}'`
UNInfo=`cat < /Volumes/DATA/_UnitsMessage/SN.txt | grep "$SN"`
UNMessage="$A""$UN"
Message="Collect Time :""$Date""$B""Bundle :""$Bundle_V""$B""Location :""$Location_""$B""Info :""$UNInfo""$B"
echo $Message >> /Volumes/DATA/Regression_Log/$Location/UnitsMessage.txt
mkdir /private/var/root/Desktop/$UNMessage
mv /private/var/root/Desktop/*.tgz /private/var/root/Desktop/$UNMessage
cd /private/var/root/Desktop
mv *.png $Location_.png
mv /private/var/root/Desktop/*.png /private/var/root/Desktop/$UNMessage
/Volumes/DATA/_Script/Touch_WIP.sh
cp -rf /private/var/root/Desktop/$UNMessage /Volumes/DATA/Regression_Log/$Bundle_V
cp -rf /private/var/root/Desktop/$WIP /Volumes/DATA/Regression_Log/$Bundle_V/$UNMessage
sleep 3
killall -m Terminal 
exit 0
fi
done
echo;echo "\033[31m No Match SN !!!";echo "\033[30m";echo;exit 1