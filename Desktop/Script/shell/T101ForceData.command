#!/bin/sh

open /TE_Support/Tools/T101ForceData.app
#open /TE_Support/Tools/T101ForceData.app
sleep 2

Product=""
Ypc=/AppleInternal/Diagnostics/Tools/ypc2
echo "Checking Product Name"
kvalue=`$Ypc -rk RPlt`
Product=`echo $kvalue |xxd -p -r|awk '{print toupper($0)}'`
Stage="Preburn"
echo "System Platform is: $Product"
BuildStage=Proto3

TimeStamp=`date +%Y_%m_%d_%H_%M_%S`

if [[ -s /Phoenix/Logs/SerialNumber.txt ]];then
	SystemSerialNumber=`cat /Phoenix/Logs/SerialNumber.txt`
else
 	SystemSerialNumber="NoSystemSN"
fi

if [[ -s /Phoenix/Logs/Trackpad_SN.txt ]];then
	TrackpadSerialNumber=`cat /Phoenix/Logs/Trackpad_SN.txt`
else
 	TrackpadSerialNumber="NoTrackpadSN"
fi


screencapture /private/var/root/Desktop/SkyNet_"$Product"_"$Stage"_"T101Force"_"$SystemSerialNumber"-"$TrackpadSerialNumber"_"$TimeStamp".png
#screencapture ~/Desktop/SkyNet_"$Product"_"$Stage"_"T101Force"_"$SystemSerialNumber"-"$TrackpadSerialNumber"_"$TimeStamp".png

sleep 2
cp /private/var/root/Desktop/SkyNet_"$Product"_"$Stage"_"T101Force"_"$SystemSerialNumber"-"$TrackpadSerialNumber"_"$TimeStamp".png /Phoenix/Logs/
cp /private/var/root/Desktop/SkyNet_"$Product"_"$Stage"_"T101Force"_"$SystemSerialNumber"-"$TrackpadSerialNumber"_"$TimeStamp".png /Phoenix/tmp/
#cp ~/Desktop/SkyNet_"$Product"_"$Stage"_"T101Force"_"$SystemSerialNumber"-"$TrackpadSerialNumber"_"$TimeStamp".png /Phoenix/Logs/
#cp ~/Desktop/SkyNet_"$Product"_"$Stage"_"T101Force"_"$SystemSerialNumber"-"$TrackpadSerialNumber"_"$TimeStamp".png /Phoenix/tmp/

killall -m T101ForceData
