#!/bin/sh
#SWDL would fail if coredump disk is there.It only allow 5 partitions
#this script is to remove core dump disk and merge it into test partition
#

flag=`diskutil list | grep -c Apple_KernelCoreDump`
echo "flag="$flag
if [ $flag -ne 1 ];then
echo "CoreDump Disk not Found"
else 
echo "CoreDump Disk Found"
echo "Erase CoreDump Disk"
diskutil eraseVolume JHFS+ temp disk0s4
echo "Merge Coredump disk into test partition"
diskutil mergePartitions JHFS+ test disk0s3 disk0s5
fi
exit 0