#!/bin/sh
#set -x

List=`ls /Users/saseny/Downloads/Log`

#IFS='"'

for Log in $List
do 
   cd /Users/saseny/Downloads/Log
   WIP1=`cat < $Log | grep "C02" | head -1 | sed 's/.*= //' | awk -F ';' '{print$1}'`
   IFS='"'
   WIP2=`echo $WIP1 | awk -F '"' '{print$1}' | sed 's/\.*  //'`
   IFS=''
   echo "$WIP2" >> ~/Desktop/SN__.txt
done   
