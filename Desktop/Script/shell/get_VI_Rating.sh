#!/bin/sh
#
# HT Law
#
# 
# Check for Current and Voltage before proceed.
#
#
# ####################################################################################

adapter=$1
expectCurrent=4300
expectVoltage=20000


case $adapter in
"LeftRear" ) 
	opt="0x1"
	rid="0x0"
	voltageKey="D1VR"
	currentKey="D1IR"
	firmwareKey="D1if";;
"LeftFront" ) 
	opt="0x0"
	rid="0x0"
	voltageKey="D2VR"
	currentKey="D2IR"
	firmwareKey="D2if";;
"RightRear" ) 
	opt="0x0"
	rid="0x1"
	voltageKey="D3VR"
	currentKey="D3IR"
	firmwareKey="D3if";;
"RightFront" ) 
	opt="0x1"
	rid="0x1"
	voltageKey="D4VR"
	currentKey="D4IR"
	firmwareKey="D4if";;
esac


echo "\n********************************\n"`date +%Y_%m_%d_%H:%M:%S`"\n********************************"

# Reading DxVR
getVoltageRating()
{

value=`/usr/local/bin/ypc2 -rdk $voltageKey | sed 's/\..*//' | sed 's/\ //g'`
t=0
timeout=100
while [ "$value" != "$expectVoltage" ]
do
echo "[$t]`date +%Y_%M_%T`	: AC connected on [$adapter], smc voltage key is [$voltageKey], reading is [$value], expected is [$expectVoltage]"
sleep 1
value=`/usr/local/bin/ypc2 -rdk $voltageKey | sed 's/\..*//' | sed 's/\ //g'`
t=`expr $t + 1`
if [ $t -ge $timeout ];then
echo "Failed to get expected Voltage after $timeout "
exit 1
fi

done

echo "`date +%Y_%M_%T`	: AC connected on [$adapter], smc voltage key is [$voltageKey], reading is [$value], expected is [$expectVoltage]"
echo "--------------------------"
echo "Voltage: PASS !"
echo "--------------------------"

}

# Reading DxIR
getCurrentRating()
{
value=`/usr/local/bin/ypc2 -rdk $currentKey | sed 's/\..*//' | sed 's/\ //g'`
t=0
timeout=100
while [ "$value" != "$expectCurrent" ]
do
echo "[$t]`date +%Y_%M_%T`	: AC connected on [$adapter], smc current key is [$currentKey], reading is [$value], expected is [$expectCurrent]"
sleep 1
value=`/usr/local/bin/ypc2 -rdk $currentKey | sed 's/\..*//' | sed 's/\ //g'`
t=`expr $t + 1`
if [ $t -ge $timeout ];then
echo "Failed to get expected Current after $timeout "
exit 1
fi
done

echo "`date +%Y_%M_%T`	: AC connected on [$adapter], smc current key is [$currentKey], reading is [$value], expected is [$expectCurrent]"
echo "--------------------------"
echo "Current: PASS !"
echo "--------------------------"

}



#####################
# Main
#####################


getVoltageRating
getCurrentRating
exit 0
