#!/bin/bash
#set -x
DATE_H=`date +%H`
DATE_M=`date +%M`
DATE_S=`date +%S`
DATE=`date +%H:%M:%S`
line=1
A=${1}
B=${2}
C=${3}
D=${4}
E=$#

TIME_Check()
{          
while [ $DATE_H -ne $A ]
do echo $DATE;sleep 1;DATE_H=`date +%H`;DATE=`date +%H:%M:%S`
done
##
while [ $DATE_M -ne $B ] 
do echo $DATE;sleep 1;DATE_M=`date +%M`;DATE=`date +%H:%M:%S`
done
##
while [ $DATE_S -ne $C ] 
do echo $DATE;sleep 1;DATE_S=`date +%S`;DATE=`date +%H:%M:%S`
done
echo;echo " Time: $A:$B:$C Now! ";echo;echo "############################";echo "#                          #";echo "# Calculate_Time Finished! #";echo "#                          #";echo "############################";echo;echo
##
while [ $line -le $D ] 
do echo " Say: Hello ! "      
say Hello                  ## About you need the system to said like " Hello "
sleep 1
let line+=1
done 
exit 0
}
Check_A()
{
if [ -z $A ]
then
echo " No Hour input !!! ";echo;Check_B
fi  
Check_B
}
Check_B()
{
if [ -z $B ]
then
echo " No Minute input !!! ";echo;Check_C
fi 
Check_C
}
Check_C()
{
if [ -z $C ];then
echo " No Second input !!! ";echo;Check_D
fi 
Check_D
}
Check_D()
{
if [ -z $D ];then
echo " No Speak Times input !!! ";echo;exit 0
fi 
Check_H  
}
Check_H()
{
if [ $A -le 24 ];then
echo " Start !!! ";echo;sleep 1;echo " Hour Input OK ";Check_M
else echo " Hour: Input wrong time "
#Check_M
exit 0
fi
}
Check_M()
{
if [ $B -le 59 ];then
echo " Minute Input OK ";Check_S
else echo " Minute: Input wrong time "
#Check_S
exit 0
fi 
}
Check_S()
{
if [ $C -le 59 ];then
echo " Second Input OK ";Time
else echo " Second: Input wrong time "
exit 0
fi
}
Time()
{
Start;echo; echo "############################";echo "#                          #";echo "#  Calculate_Time Start!!  #";echo "#                          #";echo "############################"; TIME_Check;echo;echo
}
Start()
{
echo; echo "$E Parameters"; echo; echo "SET_TIME: ${A}:${B}:${C}  - ${D}_times"
}
echo;Check_A