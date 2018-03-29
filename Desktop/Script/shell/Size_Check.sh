#!/bin/sh
#set -x
A="\t"
Size_=`diskutil list | grep "disk0s5" | grep -c "GB"`
Size=`diskutil list | grep "disk0s5" | awk '{print$3}' | awk -F '.' '{print$1}'`

Model1=`diskutil list | grep "disk0s5" | awk '{print$3}'`
Model2=`diskutil list | grep "disk0s5" | awk '{print$4}'`
Expected="\033[32m Expected Size !!! \033[30m"
Wrong="\033[31m Wrong Size !!! \033[30m"
Result="\033[32m""Size:""$A""$Model1""$Model2""\033[30m"



if [ $Size_ -eq 1 ];then 
  if [ $Size -le 2 ];then 
  echo $Expected;echo $Result;exit 0
  else
  echo $Wrong;echo $Result;exit 1
  fi 
fi
echo $Expected;echo $Result;exit 0  



