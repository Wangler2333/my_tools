#!/bin/sh
#set -x
VB=`ls /Phoenix/Tables | grep ".tbpr*" | awk -F '.' '{print$3}'`
VB_1=`echo $VB | grep -c 1`
VB_2=`echo $VB | grep -c 2`
case $VB_1 in 
*1* )
/Volumes/DATA/Touch_Message.command
/Volumes/DATA/_Script/Pre_burn.sh
;;

*0* )
/Volumes/DATA/Touch_Message.command
/Volumes/DATA/_Script/Calculate.sh
;;
esac