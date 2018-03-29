#!/bin/sh

sleep 5

sudo kextunload /System/Library/Extensions/AmbientLightSensorOSXService.kext
sleep 1
/TE_Support/Scripts/Test_Process/start_command_c
