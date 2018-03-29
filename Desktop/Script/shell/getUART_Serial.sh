	#!/bin/sh

logPath=/Phoenix/Logs/usb_SerialUart.txt
device=$1
side=$2



getDevice() {
case $device in
"Mouse" )
	serialType="Apple Optical USB Mouse";;
"Palladium" )
	serialType="Palladium Serial"
	serialTypeExtra="FT232R USB UART";;
"Radon" )
	serialType="FT232R USB UART";;
"Xenon" )
	serialType="Xenon Serial"
	serialTypeExtra="FT232R USB UART";;
esac

case $side in
"LeftRear" ) 
	locationId1="0x14400000"
	locationId2=""
	;;
"LeftFront" ) 
	locationId1="0x14600000"
	locationId2=""
	;;
"RightRear" ) 
	locationId1="0x14100000"
	locationId2=""
	;;
"RightFront" ) 
	locationId1="0x14500000"
	locationId2=""
	;;
"LeftSide" )
	locationId1="0x14400000"
	locationId2="0x14600000"
	;;
"RightSide" )
	locationId1="0x14100000"
	locationId2="0x14500000"
	;;
"HubLeftRear" ) 
	locationId1="0x14470000"
	locationId2=""
	;;
"HubLeftFront" ) 
	locationId1="0x14670000"
	locationId2=""
	;;
"HubRightRear" ) 
	locationId1="0x14170000"
	locationId2=""
	;;
"HubRightFront" ) 
	locationId1="0x14570000"
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
#exit $rstreturn
fi

else

if [ "$locationIdCapture1" == "" ] || [ "$locationIdCapture2" == "" ];then
echo `date +%Y_%m_%d_%H:%M:%S`"\t>\tNo USB connected" >> $logPath
#exit $rstreturn
fi

fi


if [ "$locationId2" == "" ];then

if [ "$locationIdCapture1" == "$locationId1" ] || [ "$locationIdCapture2" == "$locationId1" ];then
echo `date +%Y_%m_%d_%H:%M:%S`"\t>\tCorrect, continue testing" >> $logPath
rm -rf $retryPath
exit 0
else
echo `date +%Y_%m_%d_%H:%M:%S`"\t>\tInCorrect, please continue insert to correct port" >> $logPath
#exit $rstreturn
fi

else

if [ "$locationIdCapture1" == "$locationId1" ] || [ "$locationIdCapture1" == "$locationId2" ] || [ "$locationIdCapture2" == "$locationId1" ] || [ "$locationIdCapture2" == "$locationId2" ];then
echo `date +%Y_%m_%d_%H:%M:%S`"\t>\tCorrect, continue testing" >> $logPath
rm -rf $retryPath
rstreturn=0
#exit $rstreturn
else
echo `date +%Y_%m_%d_%H:%M:%S`"\t>\tInCorrect, please continue insert to correct port" >> $logPath
#exit $rstreturn
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




