#!/bin/sh
#set -x
M8=`system_profiler SPUSBDataType | grep -c "iBridge"`;Network=`system_profiler SPUSBDataType | grep -c "Apple USB Ethernet Adapter"`;ECHO_1=" \033[31m _ - - M8 is not OK, Need Restore M8, Pls Waiting..... - - _ ";ECHO_2=" \033[30m Start Check Network.... ";ECHO_3=" Network is Ok , Start RestoreM8... ";ECHO_4=" Network is not OK , Pls check... ";ECHO_5="  \033[31m + _ - - \ Restore M8 OK! / - - _ +   ";ECHO_6=" \033[32m################################################################ ";ECHO_7=" \033[32m######################################## ";ECHO_8="\033[30m"

while [ $M8 -eq 0 ]
do 
  echo;echo $ECHO_6;echo;echo $ECHO_1;echo;echo $ECHO_6;echo;echo $ECHO_2;echo;sleep 1
       while [ $Network -eq 0 ]
       do
          echo;echo $ECHO_4;echo;echo;sleep 1
          Network=`system_profiler SPUSBDataType | grep -c "Apple USB Ethernet Adapter"`
       done
       echo;echo;echo $ECHO_3 ;echo;echo
       static-ip-address -timeout 10
       sleep 1
       restoreM8_QSMC_FATP.sh
       sleep 1
       M8=`system_profiler SPUSBDataType | grep -c "iBridge"`
done
echo;echo $ECHO_7;echo;echo $ECHO_5 ;echo;echo $ECHO_7;echo $ECHO_8;sleep 2


exit 0
      
      