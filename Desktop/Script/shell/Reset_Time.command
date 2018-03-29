#!/bin/sh

Dir=`dirname $0`

a=`diskutil list | grep -e "MaxDisk" | grep -o disk[0-9]`

bless -device /dev/"$a"s3 -setboot

cp $Dir/Tools/boot.efi /Volumes/MaxDisk
cp $Dir/Tools/LBD_startup.nsh /Volumes/MaxDisk/startup.nsh

bless --mount / --file /Volumes/MaxDisk/boot.efi --setBoot --next
nvram efi-boot-next

sleep 3

reboot