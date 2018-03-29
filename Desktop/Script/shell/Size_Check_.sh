#!/bin/sh
#set -x
Size_M=`diskutil list | grep "disk0s5" | grep -c "GB"`
Size=`diskutil list | grep "disk0s5" | awk '{print$3}' | awk -F '.' '{print$1}'`
if [ $Size_M -eq 1 ];then 
  if [ $Size -le 2 ];then 
  echo "OK";exit 0
  else
  echo "Wrong";exit 1
  fi 
fi
echo "OK";exit 0  



