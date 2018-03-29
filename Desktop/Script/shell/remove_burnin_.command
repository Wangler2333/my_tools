#!/bin/bash

external=`diskutil list | grep -c "external"`


while [ $external -eq 1 ]
do 
    external=`diskutil list | grep -c "external"`
    #echo "外接磁盘状态: "$external

done

sleep 3

expect -c "spawn eos-ssh; expect \"# \"; send \"OSDToolbox bootargs -r burnin\r\"; expect \"# \"; send \"nvram -s\r\"; expect \"# \"; send \"nvram -p\r\"; expect \"# \"; send \"reboot\r\"; expect \"# \";"

#echo "外接磁盘状态: "$external