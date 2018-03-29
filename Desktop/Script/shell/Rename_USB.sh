#!/bin/sh
#set -x
Name=`echo $0 | awk -F '/' '{print$3}'` 
if [ $Name != "DATA" ];then 
diskutil rename /Volumes/$Name DATA
echo "\033[032m[RenameUSB-OK]\033[030m"
fi