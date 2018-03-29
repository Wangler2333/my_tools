#!/bin/sh

#set -x

Log=`ls /Users/bundle/Downloads/LL`

for A in $Log
do 
   BC=`echo $A | awk -F '_' '{print$1}'`
   mkdir -p /Users/bundle/Downloads/tmp
   cp -rf /Users/bundle/Downloads/LL/$A /Users/bundle/Downloads/tmp
   
   cd /Users/bundle/Downloads/tmp 
   unzip $A
     
   if [ `cat < /Users/bundle/Downloads/tmp/$BC.log | grep -c "FAILURE_MESSAGE:ERROR"` -ne 0 ];then
       if [ `ls /Users/bundle/Downloads/Result | grep -c "$BC"` -ne 0 ];then 
          rm -rf /Users/bundle/Downloads/Result/$BC*
       fi   
       BC=`echo $A | awk -F '_' '{print$1}'`
       Name="$BC""_[FAIL]"
       mkdir -p /Users/bundle/Downloads/Result/$Name
       mv /Users/bundle/Downloads/tmp/*.png /Users/bundle/Downloads/Result/$Name
       rm -rf /Users/bundle/Downloads/tmp
       
   else  
       if [ `ls /Users/bundle/Downloads/Result | grep -c "$BC"` -ne 0 ];then 
          rm -rf /Users/bundle/Downloads/Result/$BC*
       fi  
       BC=`echo $A | awk -F '_' '{print$1}'`  
       Name="$BC""_[PASS]"
       mkdir -p /Users/bundle/Downloads/Result/$Name
       mv /Users/bundle/Downloads/tmp/*.png /Users/bundle/Downloads/Result/$Name
       rm -rf /Users/bundle/Downloads/tmp
   fi
done   