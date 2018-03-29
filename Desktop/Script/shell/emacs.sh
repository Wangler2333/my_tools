#!/bin/bash

#
declare -i var
declare -i var2=10
for var in 12 34 56  24 78 23
do 
  if [ $var -gt 56 ]
  then 
    exit 0
    #break
  fi 
echo " var value is $var "
#
echo 
while [ $var -eq 56 ]
 do 
     var2=$var
 echo " var2 value is $var2 "
     break
 done
done      
        
