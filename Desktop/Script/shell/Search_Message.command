#!/bin/sh

Dir=`dirname $0`

if [ ! -f $Dir/DefaultFile/Unitsinfo.txt ];then
 echo "\033[031m No Units Massage File, Pls check it ... \033[030m" ; exit 1 
fi 

while (true)
do 
   echo ; echo "Input search message:"
   read input 

   Result=`cat < $Dir/DefaultFile/Unitsinfo.txt | grep "$input"`
   if [ $input == "quit" ];then 
      exit 1
   fi 
   echo "------------------------"  
   i=`echo $Result | grep -c "$Build"`
   if [ $i -eq 0 ];then 
       echo "\033[031m No [\033[032m$input\033[031m] Message \033[030m"
    else
       echo "\033[032m No.       Date        Build      Config    Unit Number      WIP \033[030m" 
       echo "\033[034m $Result \033[030m"
   fi 
   
   echo "------------------------"
done 