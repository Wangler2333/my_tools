#!/bin/sh

DisplayProfileSetup=$1

case $DisplayProfileSetup in
"default" )
	DisplayProfileSetup_temp="Color LCD";;
"sRGB" )
	DisplayProfileSetup_temp="sRGB IEC61966-2.1";;
esac

echo "Setup display to $DisplayProfileSetup"
/usr/local/bin/cgdebug -displayCS $DisplayProfileSetup
sleep 1

CurrentDisplayProfile=`/usr/local/bin/cgdisplay | grep ColorProfile | sed 's/.* "//' | sed 's/"//'`

echo "Checking if display profile is correct after setup:"
echo "Expected: $DisplayProfileSetup_temp"
echo "Current : $CurrentDisplayProfile"

if [ "$$DisplayProfileSetup_temp" != "$CurrentDisplayProfile" ];then
echo "PASSED: Display profile is correct after setup"
exit 0
else
echo "FAILED: Display profile is incorrect after setup"
exit 1
fi


