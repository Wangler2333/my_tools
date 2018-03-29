#!/bin/sh

MODN=`system_profiler SPHardwareDataType | grep "Model Name:" | sed 's/.*: //'`
MODI=`system_profiler SPHardwareDataType | grep "Model Identifier:" | sed 's/.*: //'`
PROSP=`system_profiler SPHardwareDataType | grep "Processor Name:" | sed 's/.*: //'`
CPU=`system_profiler SPHardwareDataType | grep "Processor Speed" | sed 's/.*: //'`
NBPRO=`system_profiler SPHardwareDataType | grep "Number of Processors:" | sed 's/.*: //'`
TNMC=`system_profiler SPHardwareDataType | grep "Total Number of Cores:" | sed 's/.*: //'`
L2=`system_profiler SPHardwareDataType | grep "L2 Cache (per Core):" | sed 's/.*: //'`
L3=`system_profiler SPHardwareDataType | grep "L3 Cache:" | sed 's/.*: //'`
Memory=`system_profiler SPHardwareDataType | grep "Memory" | sed 's/.*: //'`
BR=`system_profiler SPHardwareDataType | grep "Boot ROM Version:" | sed 's/.*: //'`
SMC=`system_profiler SPHardwareDataType | grep "SMC Version (system):" | sed 's/.*: //'`
SerNum=`system_profiler SPHardwareDataType | grep "Serial Number (system):" | sed 's/.*: //'`
HDUU=`system_profiler SPHardwareDataType | grep "Hardware UUID:" | sed 's/.*: //'`
SSD=`system_profiler SPStorageDataType | grep "Capacity" | sed 's/.*: //'`
A="\n"
Message="Model Name: ""$MODN""$A""Model Identifier: ""$MODI""$A""Processor Name: ""$PROSP""$A""Processor Speed: ""$CPU""$A""Number of Processors: ""$NBPRO""$A""Total Number of Cores: ""$TNMC""$A""L2 Cache (per Core): ""$L2""$A""L3 Cache: ""$L3""$A""Memory: ""$Memory""$A""Boot ROM Version: ""$BR""$A""SMC Version (system): ""$SMC""$A""Serial Number (system): ""$SerNum""$A""Hardware UUID: ""$HDUU""$A""Storage: ""$SSD"
Name="$SerNum"_"Message"
#echo "$isConnected" 
#if [ "$isConnected" == "Yes" ];then
#echo "AC connected ... !"
#exit 0
#else
#echo "AC not connected"
#exit 1
#fi

Check()
{
if [ "$Memory" == "8 GB" ];then

echo ""
echo ""
echo "***** O 8 GB O *****"
echo ""
echo ""

else
echo "***** -- *****"
exit
fi
}
{
if [ "$Memory" == "16 GB" ];then
echo "***** 16 GB *****"
else
echo "***** -- *****"
Check
fi
}


echo "$Memory"

echo $Message > /Users/saseny/Desktop/$Name.txt
