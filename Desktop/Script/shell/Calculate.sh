#!/bin/sh
#set -x
N="1"
A=`ls /Volumes/DATA | grep -c "tmp"`
if [ $A = 0 ];then  
mkdir /Volumes/DATA/tmp
echo "\033[31m How many Units going to Run_in Test ? \033[30m"
read Number
echo $Number > /Volumes/DATA/tmp/Total.txt
Full=$(($Number/3))
echo $Full > /Volumes/DATA/tmp/Full.txt
None=$(($Number-$Full))
echo $None > /Volumes/DATA/tmp/None.txt
fi
Number=`cat < /Volumes/DATA/tmp/Total.txt`
Full=`cat < /Volumes/DATA/tmp/Full.txt`
None=`cat < /Volumes/DATA/tmp/None.txt`
echo $N >> /Volumes/DATA/tmp/N.txt
echo "\033[31m Run_in Total : $Number   Full : $Full  None : $None \033[30m"
Times=`cat < /Volumes/DATA/tmp/N.txt | grep -c "1"`
echo $Times
if [ $Times -le $Full ];then 
echo "\033[32m Copy Full Tables \033[30m"
/Volumes/DATA/_Script/Run_in_F.sh
else
echo "\033[32m Copy None Tables \033[30m"
/Volumes/DATA/_Script/Run_in_N.sh
fi 
if [ $Times -eq $Number ];then 
rm -rf /Volumes/DATA/tmp
fi 