#!/bin/sh


rm -rf /System/Library/Extensions/AmbientLightSensorOSXService.kext
rm -Rf /System/Library/Caches/*.*
sync
sync
sync
touch /System/Library/Extensions

reboot