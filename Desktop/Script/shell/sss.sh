#!/bin/bash

set -x

DATE_H=`date +%H`
DATE_M=`date +%M`
DATE_S=`date +%S`
DATE=`date +%H:%M:%S`
line=1
A=${1}
B=${2}
C=${3}
D=${4}
##################
TIME_Check()
{          
while [ $DATE_H -ne $A ]
do 
echo $DATE
#echo " Time Not OK 1 "
sleep 1
DATE_H=`date +%H` 
DATE=`date +%H:%M:%S`
done 
##
while [ $DATE_M -ne $B ]
do 
echo $DATE
#echo " Time Not OK 2 "
sleep 1
DATE_M=`date +%M`
DATE=`date +%H:%M:%S`
done
##
while [ $DATE_S -ne $C ]
do 
echo $DATE
#echo " Time Not OK 3 "
sleep 1
DATE_S=`date +%S`
DATE=`date +%H:%M:%S`
done
echo " Time: $A:$B:$C Now! "
echo
echo "############################"
echo "#                          #"
echo "# Calculate_Time Finished! #"
echo "#                          #"
echo "############################"
echo
##
while [ $line -le $D ]    
do 
echo " Say: Hello ! "      
say Hello                  ## About you need the system to said like " Hello "
sleep 1
let line+=1
done 
exit 0
}
##################
Check_H()
{
if [ -n $A ]
then 
  echo " No Hour input !!! "
  echo 
  exit 0
fi  
if [ $A -le 24 ]
  then
    echo " Hour Input OK "
    Check_M
  else 
    echo " Hour: Input wrong time "
    Check_M
  exit 0
fi
}
Check_M()
{
if [ -n $B ]
then 
  echo " No Minute input !!! "
  echo 
  exit 0
fi 
if [ $B -le 59 ] 
  then 
    echo " Minute Input OK "
    Check_S
  else 
    echo " Minute: Input wrong time "
    Check_S
  exit 0 
fi 
}
Check_S()
{
if [ -n $C ]
then 
  echo " No Second input !!! "
  echo 
  exit 0
fi 
if [ $C -le 59 ]
  then 
    echo " Second Input OK "
    Time
  else 
    echo " Second: Input wrong time "
fi
}
Time()
{    
if [ -n $D ]
then 
  echo " No Speak Times input !!! "
  echo 
  exit 0
fi     
    echo
    echo "############################"
    echo "#                          #"
    echo "#  Calculate_Time Start!!  #"
    echo "#                          #"
    echo "############################"
    #sleep 1
    TIME_Check
    echo
    echo
} 
##################
echo 
echo 
if [ -z $@ ]
then 
  echo " No input ? ! ? "
  echo 
else 
  echo " Start !!! "
  echo 
  Check_H
fi
  