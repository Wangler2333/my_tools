#!/bin/sh

Kill1()
{
killall -m VirtualBoxVM
}
Kill2()
{
killall -m VirtualBox
}
Read()
{
echo
echo " Pls choose continue kill VirtualBox (Y/N) "
echo
read -e continue
if [ $continue = Y ]
then 
  echo 
  echo " Kill VirtualBoxVM Now ! "
  echo 
  sleep 1
  Kill2
  echo   
else
  echo " Don't Kill ! "
  sleep 1
  exit 0
fi  
}
  
##### Main Script ######  
echo
echo " Pls choose continue kill VirtualBoxVM (Y/N) "
echo
read -e continue
if [ $continue = Y ] 
then 
  echo 
  echo " Kill VirtualBox Now ! "
  echo 
  sleep 1
  Kill1
  echo 
  Read  
else
  echo " Don't Kill ! "
  sleep 1
  exit 0
fi
######################## 