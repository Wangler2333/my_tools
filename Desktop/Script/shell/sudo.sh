#!/bin/sh

read -e A
while [ $A !=Y ] && [ $A !=N ]
do 
echo " Pls int something Y or N "
sleep 1
done

read -e A
if [ $A != Y ];then
 echo " No "
 exit
fi 



diskutil list