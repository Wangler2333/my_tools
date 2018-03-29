#!/bin/sh
# Developed by Ferris Feng.
# 08-12-2014 Initial release v1.0

scriptVersion="1.0"

# Get display panel serial number using PanelDetect tool.
panelDetectOutput=`/Indy/Runtime_Files/OS/TestApps/PanelDetect.app/Contents/MacOS/PanelDetect -c`
programmedDisplaySN=`echo "${panelDetectOutput}" | grep -i 'Serial' | cut -d : -f 2 | sed 's/[[^ ]]*//g'`
if [ `echo $?` -ne 0 ]; then
    echo "Errow with parsing programmed SN using tool PanelDetect."
    exit -1
fi
# Call plistParser to modify /Phoenix/Configuration/unit_settings.plist
/Phoenix/Tools/plistparser file: /Phoenix/Configuration/unit_settings.plist key: Comm.Send.TestEnvInfo:LCDSN set: "${programmedDisplaySN}"
if [ `echo $?` -ne 0 ]; then
    echo "Errow with inserting display panel serial number into /Phoenix/Configuration/unit_settings.plist"
    exit -2
fi

