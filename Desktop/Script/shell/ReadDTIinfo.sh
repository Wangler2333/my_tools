#!/bin/sh

#  $1 input    $2 output

Pathroad=$1

[ ! -f $2 ] && echo "Serial Number,EECode,WIP,Bundle,OS,PhoenixCE,BootRom,SMC,MacAddress" >> $2

TotalMesg=`cat < $Pathroad | grep "DTI" | tail -1`

PhoenixCE=`echo $TotalMesg | sed 's/.*PhoenixOS=//' | awk -F ',' '{print$1}' | sed 's/\"//g'`
OSVersion=`echo $TotalMesg | sed 's/.*OSVersion=//' | awk -F ',' '{print$1}' | sed 's/\"//g'`
Bundlename=`echo $TotalMesg | sed 's/.*Bundle=//' | awk -F ',' '{print$1}' | sed 's/\"//g'`
BootROM=`echo $TotalMesg | sed 's/.*BootROM=//' | awk -F ',' '{print$1}' | sed 's/\"//g'`
SMC=`echo $TotalMesg | sed 's/.*SMC=//' | awk -F ',' '{print$1}' | sed 's/\"//g'`
MacAddress=`echo $TotalMesg | sed 's/.*MacAddress=//' | awk -F ',' '{print$1}' | sed 's/\"//g'`
WIPNo=`echo $TotalMesg | sed 's/.*WIPNo=//' | awk -F ',' '{print$1}' | sed 's/\"//g'`
HWC=`echo $TotalMesg | sed 's/.*HWC=//' | awk -F ',' '{print$1}' | sed 's/\"//g'`

#echo $WIPNo
#echo $PhoenixCE
#echo $OSVersion
#echo $Bundlename
#echo $BootROM
#echo $SMC
#echo $MacAddress
#echo $HWC

SerialNumber=`echo $WIPNo | awk -F '+' '{print$1}'`

#echo $SerialNumber

echo "$SerialNumber,$HWC,$WIPNo,$Bundlename,$OSVersion,$PhoenixCE,$BootROM,$SMC,$MacAddress" >> $2


