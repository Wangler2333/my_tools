#!/bin/sh
#Kaiser Yuan 2016-01-26
#Foramt Xenon New Port disk with Name "Xenon SerialNumber"

flag=`system_profiler SPUSBDataType |grep -c "Xenon New Port"`
if [ $flag -eq 1 ];then
{
    XenonSN=$(system_profiler SPUSBDataType | grep "Serial"| awk -F" " '{print $3}')
    Name="Xenon "$XenonSN

    echo "\033[1;32m $Name \033[0m"
    
    diskutil eraseVolume JHFS+ "$Name" /dev/disk1s2
    }
    else echo "\033[1;32m Xenon New Port not Connected \033[0m"
    fi
