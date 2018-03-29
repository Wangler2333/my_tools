#!/bin/sh

Status=`/usr/local/bin/lha /AppleInternal/Diagnostics/Tools/Usb/USBTestScripts/usb_lua/usb-config.lua --show=1 | grep "Port 1" | grep "Connected"`

returnValue=`echo $?`

if [ $returnValue -eq 0 ];then
echo "Left USB3.0 detected"
exit 0
else
echo "Left USB3.0 not detected"
exit 1
fi




