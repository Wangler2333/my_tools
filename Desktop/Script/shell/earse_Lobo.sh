#!/bin/sh

disk_info=`diskutil apfs list | grep "APFS Container Reference" | sed 's/.*: //' | sed 's/ //g'`
cm_disk=`diskutil list external | grep "Apple_HFS Macintosh HD" | awk '{print $NF}'`

for i in $disk_info
do 
    echo $i
    diskutil apfs deleteContainer $i  
done

for j in $cm_disk
do 
    echo $j
    sudo diskutil eraseVolume JHFS+ Noname /dev/$j
done    