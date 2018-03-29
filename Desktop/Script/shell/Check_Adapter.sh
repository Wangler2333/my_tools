#!/bin/sh
#set -x
Adapter=$1
case $Adapter in
"LR" ) 
	voltageKey="D1VR"
	currentKey="D1IR"
	firmwareKey="D1if";;
"LF" ) 
	voltageKey="D2VR"
	currentKey="D2IR"
	firmwareKey="D2if";;
"RR" ) 
	voltageKey="D3VR"
	currentKey="D3IR"
	firmwareKey="D3if";;
"RF" ) 
	voltageKey="D4VR"
	currentKey="D4IR"
	firmwareKey="D4if";;
esac
F_value=`/usr/local/bin/ypc2 -drk $firmwareKey | sed 's/\..*//'`
V_Check()
{
V_value=`/usr/local/bin/ypc2 -drk $voltageKey | sed 's/\..*//'`
while [ $V_value -eq 0 ]
do 
echo "\033[031m No Adapter Detected ! \033[030m" ; sleep 1
V_value=`/usr/local/bin/ypc2 -drk $voltageKey | sed 's/\..*//'`
done
echo "\033[032m Voltage : $V_value \033[030m"
}
C_Check()
{
C_value=`/usr/local/bin/ypc2 -drk $currentKey | sed 's/\..*//'`
while [ $C_value -eq 0 ]
do
echo "\033[031m No Adapter Detected ! \033[030m" ; sleep 1
C_value=`/usr/local/bin/ypc2 -drk $currentKey | sed 's/\..*//'`
done
echo "\033[032m Current : $C_value \033[030m"
}

##############
V_Check
C_Check
echo "\033[032m Firmware : $F_value \033[030m"
exit 0

