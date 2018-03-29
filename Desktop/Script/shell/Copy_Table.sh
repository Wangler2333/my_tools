#!/bin/sh
set -x
/Users/sasenyzhou/Desktop/_Script/CheckDate.sh
Bundle=`ls /Phoenix/Tables | grep "PGQ" | awk -F '.tb*' '{print$1}'`
ABC=`echo $Bundle | awk -F '.' '{print$4}'`
Pre_burn=`echo $ABC | grep -c "1"`
Run_in=`echo $ABC | grep -c "2"`

if [ $Pre_burn = 1 ];then 
echo " Copy Pre_burn Tables .... "
exit 0
fi 
if [ $Run_in = 1 ];then 
echo " Copy Run_in Table .... "
/Volumes/DATA/_Script/calculate.sh
exit 1
fi 
echo " No normal Table , Pls check it .... "