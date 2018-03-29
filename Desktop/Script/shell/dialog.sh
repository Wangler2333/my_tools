#!/bin/bash
#
dialog --yesno "Do you want to continue? " 9 36
choose=$?
if [ choose -ne 0 ]
then 
  answer=no 
else
  answer=yes
fi
#
default=no
if [ $answer = $default ]
then 
  dialog --msgbox " Stop continue... "
else
  dialog --yesno " Are you ture? " 8 28
  echo 
  echo " Please wait... "
  echo ; sleep 1
#
  {
   for ((time=1 ; time<=10 ; time++))
   do 
     let TIME=10*time
     echo $TIME
     sleep 1
   done
   } |
   dialog --guage " Rate of progress... " 6 36
fi 
exit 0    
        