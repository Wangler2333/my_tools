#!/bin/sh

logPath=/Phoenix/Logs/usb_SerialUart.txt
device=$1
side=$2


getDevice() {
case $device in
"Xenon" )
	serialType="Xenon Legacy Port"
	serialTypeExtra="FT232R USB UART";;
esac

case $side in
"LeftRear" ) 
	locationId1="0x00400000"
	locationId2=""
	;;
"LeftFront" ) 
	locationId1="0x00300000"
	locationId2=""
	;;
"RightRear" ) 
	locationId1="0x01300000"
	locationId2=""
	;;
"RightFront" ) 
	locationId1="0x01400000"
	locationId2=""
	;;	

esac

}


dumpSystemDevice() {

echo `date +%Y_%m_%d_%H:%M:%S`"\t>\tYou are connecting to [$serialType]" >> $logPath
if [ "$locationId2" == "" ];then

locationIdCapture1=`system_profiler SPUSBDataType | grep -A15 "$serialType" | grep "Location ID" | sed 's/.*: //' | sed 's/ \/.*//' | head -1`

#workaround for Palladium box which have 2 differents serial name
if [ "$locationIdCapture1" == "" ];then
locationIdCapture1=`system_profiler SPUSBDataType | grep -A15 "$serialTypeExtra" | grep "Location ID" | sed 's/.*: //' | sed 's/ \/.*//' | head -1`
fi

locationIdCapture2=`system_profiler SPUSBDataType | grep -A15 "$serialType" | grep "Location ID" | sed 's/.*: //' | sed 's/ \/.*//' | tail -1`

echo `date +%Y_%m_%d_%H:%M:%S`"\t>\tCurrent location ID capture: [$locationIdCapture1], expecting [$locationId1]" >> $logPath
else

locationIdCapture1=`system_profiler SPUSBDataType | grep -A15 "$serialType" | grep "Location ID" | sed 's/.*: //' | sed 's/ \/.*//' | head -1`
locationIdCapture2=`system_profiler SPUSBDataType | grep -A15 "$serialType" | grep "Location ID" | sed 's/.*: //' | sed 's/ \/.*//' | tail -1`

#workaround for Palladium box which have 2 differents serial name
if [ "$locationIdCapture1" == "" ];then
locationIdCapture1=`system_profiler SPUSBDataType | grep -A15 "$serialTypeExtra" | grep "Location ID" | sed 's/.*: //' | sed 's/ \/.*//' | head -1`
fi
if [ "$locationIdCapture2" == "" ];then
locationIdCapture2=`system_profiler SPUSBDataType | grep -A15 "$serialTypeExtra" | grep "Location ID" | sed 's/.*: //' | sed 's/ \/.*//' | tail -1`
fi

echo `date +%Y_%m_%d_%H:%M:%S`"\t>\tCurrent location ID capture: [$locationIdCapture1] and [$locationIdCapture2], expecting [$locationId1] OR [$locationId2]" >> $logPath
fi
}

checkResult() {

rstreturn=1

if [ "$locationId2" == "" ];then

if [ "$locationIdCapture1" == "" ];then
echo `date +%Y_%m_%d_%H:%M:%S`"\t>\tNo USB connected" >> $logPath
#
rm -rf $retryPath
rstreturn=0
#
fi

else

if [ "$locationIdCapture1" == "" ] || [ "$locationIdCapture2" == "" ];then
echo `date +%Y_%m_%d_%H:%M:%S`"\t>\tNo USB connected" >> $logPath
#
rm -rf $retryPath
rstreturn=0
#
fi

fi

}

countNumberOfRetry() {

retryPath=/Phoenix/Logs/RetryCount.txt
maxRetry=5

if [ ! -f $retryPath ];then
touch $retryPath
fi

retryInt=`cat $retryPath`

if [ "$retryInt" == "" ];then
retryInt=0
fi

retryInt=`expr $retryInt + 1`
echo $retryInt > $retryPath

echo `date +%Y_%m_%d_%H:%M:%S`"\t>\tNumber Of Retry = [ $retryInt ]" >> $logPath

if [ "$retryInt" -ge "$maxRetry" ];then
echo `date +%Y_%m_%d_%H:%M:%S`"\t>\tExceed max allowed retry [ $retryInt / $maxRetry ]!" >> $logPath
rm -rf $retryPath
exit 0
else
echo `date +%Y_%m_%d_%H:%M:%S`"\t>\tWithin max retry [ $retryInt / $maxRetry ]" >> $logPath
fi

}

# ======================================================
# Main Routine
#
# HT Law, June 16
# ======================================================
countNumberOfRetry
getDevice
dumpSystemDevice
checkResult

while [ "$rstreturn" -ne 0 ]
do
dumpSystemDevice
checkResult
sleep 1

done

sleep 2
exit 0