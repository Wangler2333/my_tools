#!/bin/sh
set -x 
#diskutil renameVolume disk1s2 DATA
#/TE_Support/Tools/Phoenix/COPYLOGS.pl
Location="_Pre-Burn"      ##  _Pre-Burn  _Run-In  _Post-Burn
SystemSN=`system_profiler SPHardwareDataType | grep Serial | awk -F ':' '{print$2}'`
SNMessage=`cat < /Volumes/DATA/_UnitsMessage/SN.txt | awk -F ';' '{print$2}'`
Bundle_V=`ls /Phoenix/Tables | grep "PGQ" | awk -F '.tb*' '{print$1}'`
Date=`date +%Y-%m-%d--%H:%M:%S`
Location_=`echo $Location | awk -F '_' '{print$2}'`
A="#"
B="\n"

if [ -z $SystemSN ];then 
SystemSN=`cat < /Phoenix/Logs/state.txt | grep "WIP" | awk '{print$6}' | awk -F '+' '{print$1}'`
fi 
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
WIP1=`cat < /Volumes/DATA/_UnitsMessage/SN.txt | grep "$SN" | awk -F ';' '{print$2}'`
WIP2=`cat < /Volumes/DATA/_UnitsMessage/SN.txt | grep "$SN" | awk -F ';' '{print$3}'`
WIP="$WIP1""+""$WIP2"
touch /private/var/root/Desktop/$WIP
cp -rf /private/var/root/Desktop/$UNMessage /Volumes/DATA/Regression_Log/$Location
sleep 2
killall -m Terminal 
exit 0
fi
done
echo;echo "\033[31m No Match SN !!!";echo "\033[30m";echo;exit 1
