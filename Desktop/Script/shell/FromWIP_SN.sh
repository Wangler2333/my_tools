#!/bin/sh
#set -x
## 修改WIP，保留SN

if [ -z $1 ];then
Path="/Users/bundle/Downloads/LL_DOE.txt"
else
Path=$1
fi

WIP=`cat < $Path`

Path=`echo $0 | awk -F 'FromWIP_SN.sh' '{print$1}'`
B=0
for A in $WIP
do 
  
   SN=`echo $A | head -c 12`   
   
   EX=`cat < $Path/LL.txt`
   case $EX in
   *$SN* )
   echo "SN Exist!"
   ;;
   *)
   let B=$B+1
   #echo "$SN" "[$B]"
   echo $SN >> $Path/LL.txt
   ;;
   esac
   
done   

echo "Total:[$B]"