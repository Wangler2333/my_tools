#!/bin/sh

Dir=`dirname $0`
DISK=$1
testbundle=$2
cmbundle=$3

DISK_=$DISK"s3"
DISK_1=$DISK"s5"
DISK_2=$DISK"s4"


# command  1
sudo diskutil partitionDisk /dev/$DISK 1 GPTFormat hfs+ NoName 1G
if [ $? -eq 0 ];then
   echo "Pass_1" > $Dir/$DISK.txt
else
   echo "Fail_1" > $Dir/$DISK.txt
   exit 1
fi


# command  2
sudo /usr/sbin/asr partition --target /dev/$DISK --testsize 71g --retestsize 1g --recoverysize 80g
if [ $? -eq 0 ];then
   echo "Pass_2" > $Dir/$DISK.txt
else
   echo "Fail_2" > $Dir/$DISK.txt
   exit 1
fi


# command  3
#sudo diskutil resizeVolume /dev/$DISK_ 70g %5361644d-6163-11AA-AA11-00306543ECAC% KernelCore 1g
if [ $? -eq 0 ];then
   echo "Pass_3" > $Dir/$DISK.txt
else
   echo "Fail_3" > $Dir/$DISK.txt
   exit 1
fi


# command  4
sudo diskutil eraseVolume hfs+ Apple_Boot /dev/$DISK_1
if [ $? -eq 0 ];then
   echo "Pass_4" > $Dir/$DISK.txt
else
   echo "Fail_4" > $Dir/$DISK.txt
   exit 1
fi


# command  5
sudo diskutil unmount force /dev/$DISK_1
if [ $? -eq 0 ];then
   echo "Pass_5" > $Dir/$DISK.txt
else
   echo "Fail_5" > $Dir/$DISK.txt
   exit 1
fi


# command  6
sudo asr adjust --target /dev/$DISK_1 --settype apple_kfs
if [ $? -eq 0 ];then
   echo "Pass_6" > $Dir/$DISK.txt
else
   echo "Fail_6" > $Dir/$DISK.txt
   exit 1
fi

# command  7
sudo diskutil unmount force /dev/$DISK_2
if [ $? -eq 0 ];then
   echo "Pass_7" > $Dir/$DISK.txt
else
   echo "Fail_7" > $Dir/$DISK.txt
   exit 1
fi


# command  8
sudo /usr/sbin/asr restore --target /dev/$DISK_ --source $testbundle --erase --noprompt --puppetstrings --noverify
if [ $? -eq 0 ];then
   echo "Pass_8" > $Dir/$DISK.txt
else
   echo "Fail_8" > $Dir/$DISK.txt
   exit 1
fi


# command  9 
sudo diskutil unmountDisk force /dev/$DISK
if [ $? -eq 0 ];then
   echo "Pass_9" > $Dir/$DISK.txt
else
   echo "Fail_9" > $Dir/$DISK.txt
   exit 1
fi


# command  10
sudo diskutil mount /dev/$DISK
if [ $? -eq 0 ];then
   echo "Pass_10" > $Dir/$DISK.txt
else
   echo "Fail_10" > $Dir/$DISK.txt
   exit 1
fi


if [ ! -z $cmbundle ];then

    # command  11
    sudo diskutil rename /dev/$DISK_ $DISK
    if [ $? -eq 0 ];then
       echo "Pass_11" > $Dir/$DISK.txt
    else
       echo "Fail_11" > $Dir/$DISK.txt
       exit 1
    fi

    # command  12
    sudo ditto -rsrcFork $cmbundle /Volumes/$DISK
    if [ $? -eq 0 ];then
       echo "Pass_12" > $Dir/$DISK.txt
    else
       echo "Fail_12" > $Dir/$DISK.txt
       exit 1
    fi

    # command  13
    sudo diskutil rename /dev/$DISK_ MaxDisk
    if [ $? -eq 0 ];then
       echo "Pass_13" > $Dir/$DISK.txt
    else
       echo "Fail_13" > $Dir/$DISK.txt
       exit 1
    fi
    
fi

echo "Finished" > $Dir/$DISK.txt
