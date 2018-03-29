#!/bin/sh
echo "Copying logs file"
SerNum=`system_profiler SPHardwareDataType | grep "Serial Number" | sed 's/.*: //'`"_ShmooLog"
cd /private/var/root/Desktop
mkdir /private/var/root/Desktop/$SerNum

#mv S2* /private/var/root/Desktop/$SerNum
mv MmaLogDOE* /private/var/root/Desktop/$SerNum

cp -rf /private/var/root/Desktop/$SerNum /Volumes/HD