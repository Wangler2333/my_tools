#!/bin/sh
DATE=`date +%Y-%m-%d_%H:%M:%S`

MN=`system_profiler SPHardwareDataType | grep "Model Name" | sed 's/.*: //'`             
MI=`system_profiler SPHardwareDataType | grep "Model Identifier" | sed 's/.*: //'`
PN=`system_profiler SPHardwareDataType | grep "Processor Name" | sed 's/.*: //'`
PS=`system_profiler SPHardwareDataType | grep "Processor Speed" | sed 's/.*: //'`
NoP=`system_profiler SPHardwareDataType | grep "Number of Processors" | sed 's/.*: //'`
TNoC=`system_profiler SPHardwareDataType | grep "Total Number of Cores" | sed 's/.*: //'`
L2C=`system_profiler SPHardwareDataType | grep "L2 Cache" | sed 's/.*: //'`
L3C=`system_profiler SPHardwareDataType | grep "L3 Cache" | sed 's/.*: //'`
Memory=`system_profiler SPHardwareDataType | grep "Memory" | sed 's/.*: //'`
BRV=`system_profiler SPHardwareDataType | grep "Boot ROM" | sed 's/.*: //'`
SMC=`system_profiler SPHardwareDataType | grep "SMC" | sed 's/.*: //'`
SerNum=`system_profiler SPHardwareDataType | grep "Serial Number" | sed 's/.*: //'`
HUU=`system_profiler SPHardwareDataType | grep "Hardware UUID" | sed 's/.*: //'`
Storage=`system_profiler SPStorageDataType | grep "Capacity" | sed 's/.*: //'`
MT=`system_profiler SPStorageDataType | grep "Medium Type" | sed 's/.*: //'`

#VRAM=`cat < /Users/SasenyZhou/Desktop/123.txt | grep "Saseny" | sed 's/.*: //'`
#PLW=`system_profiler SPGraphics/DisplaysDataType | grep "PCIe Lane Width" | sed 's/.*: //'`
A="\n"

Name1="Model Name : ""$MN""$A"
Name2="Model Identifier : ""$MI""$A"
Name3="Processor Name : ""$PN""$A"
Name4="Processor Speed : ""$PS""$A"
Name5="Number of Processors : ""$NoP""$A"
Name6="Total Number of Cores : ""$TNoC""$A"
Name7="L2 Cache : ""$L2C""$A"
Name8="L3 Cache : ""$L3C""$A"
Name9="Memory : ""$Memory""$A"
Name10="Boot ROM : ""$BRV""$A"
Name11="SMC : ""$SMC""$A"
Name12="Serial Number : ""$SerNum""$A"
Name13="Storage : ""$MT ""$Storage""$A"
Name14="Hardware UUID : ""$HUU""$A"
#Name15="VRAM(Total)_PCIe Lane Width : ""$VRAM"##_"$PLW"
#Name15="$VRAM"

Name="Saseny : ""$DATE""$A""$Name1""$Name2""$Name3""$Name4""$Name5""$Name6""$Name7""$Name8""$Name9""$Name10""$Name11""$Name12""$Name13""$Name14"
File="$SerNum"_"$DATE"

echo $Name > /Users/SasenyZhou/Desktop/prince/TXT/$File.txt

#cd /Users/SasenyZhou/Desktop/Script
#zip -r $SerNum.zip ./*
#zip 123.zip 123.txt
#zip CD.zip 12345.command
# cd /Users/SasenyZhou/Desktop/Script
# unzip -o -d /Users/SasenyZhou/Desktop/Script CD.zip

cd /Users/SasenyZhou/Desktop/prince/TXT/
cat < $File.txt >> All.txt

123()
{
ABC()
{
echo $Name > /Users/SasenyZhou/Desktop/Script/$File.txt
sleep 15
ABCD
}
ABCD()
{
cd /Users/SasenyZhou/Desktop/Script
ls 123.txt
if [ $? -eq 0 ];then
 echo "HAVE"
 sleep 1
 echo $Name > /Users/SasenyZhou/Desktop/Script/$File.txt
 sleep 3
 ABCD
else
 echo "NO"
 exit 0
fi  

}
1234()
{
cd /Users/SasenyZhou/Desktop/Script
ls 123.txt
if [ $? -eq 0 ];then
 echo "HAVE"
 ABC
else
 echo "NO"
 exit 0
fi  

}
