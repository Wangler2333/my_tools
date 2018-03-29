#!/bin/sh

SN=`cat < /Phoenix/Logs/SerialNumber.txt`
SerNum=`system_profiler SPHardwareDataType | grep "Serial Number" | sed 's/.*: //'`
DATE=`date +%Y_%m_%d@%H-%M-%S`
SN1="$SN"@"$DATE"
SN2="$SerNum"_"$DATE"

dispplayResult()                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         
{
	echo "6. Display Result"

	echo -e "\033[32m==================================================="
	echo -e "\033[32m           *****   ***   *****  *****              "
	echo -e "\033[32m           *   *  *   *  *      *                  "
	echo -e "\033[32m           *****  *****  *****  *****              "
	echo -e "\033[32m           *      *   *      *      *              "
	echo -e "\033[32m           *      *   *  *****  *****              "
	echo -e "\033[32m==================================================="

}

mkdir /Volumes/Download/Logs/$SN
mkdir /Volumes/Download/Logs/op
cp -rf /Phoenix/Logs /Volumes/Download/Logs/op
cd /Volumes/Download/Logs/op
mv Logs PhoenixLogs
zip -r PhoenixLogs.zip ./*
rm -rf /Volumes/Download/Logs/op/PhoenixLogs
mv /Volumes/Download/Logs/op/PhoenixLogs.zip /Volumes/Download/Logs/$SN
cp -rf /AppleInternal/Diagnostics/Logs /Volumes/Download/Logs/op
cd /Volumes/Download/Logs/op
mv Logs DiagnosticsLogs
zip -r DiagnosticsLogs.zip ./*
rm -rf /Volumes/Download/Logs/op/DiagnosticsLogs
mv /Volumes/Download/Logs/op/DiagnosticsLogs.zip /Volumes/Download/Logs/$SN
cp -rf /Library/Logs /Volumes/Download/Logs/op  
cd /Volumes/Download/Logs/op
mv Logs LibraryLogs
zip -r LibraryLogs.zip ./* 
rm -rf /Volumes/Download/Logs/op/LibraryLogs  
mv /Volumes/Download/Logs/op/LibraryLogs.zip /Volumes/Download/Logs/$SN

screencapture /Volumes/Download/Logs/$SN/$SN.png


rm -rf /Volumes/Download/Logs/op
cd /Volumes/Download/Logs/
zip -r $SN1.zip $SN
rm -rf /Volumes/Download/Logs/$SN

dispplayResult



#echo " CopyLog "
#ls /Phoenix/Logs/SerialNumber.txt
#   if [ $? -eq 0 ]; then
#      echo " Have SerialNumber.txt "
#      CopyLog1 
#      exit 0    
#   else 
#      echo " No SerialNumber.txt " 
#      CopyLog2
#      exit 0
