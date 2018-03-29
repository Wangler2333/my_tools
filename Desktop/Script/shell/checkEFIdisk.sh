#!/bin/sh

diskMount=`df | grep "disk0s1" | awk -F ' ' '{print $NF}'`
echo "Disk disk0s1 mounted: $diskMount"

if [ "$diskMount" == "/Volumes/EFI" ];then

echo "Unmount disk : $diskMount"
diskutil unmount disk0s1

fi
