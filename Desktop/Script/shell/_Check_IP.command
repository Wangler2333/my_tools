#!/bin/sh

FailMessage()
{
	echo  "\033[31m=======================================\033[30m"
	echo  "\033[31m       *****   ***   *****  *          \033[30m"
	echo  "\033[31m       *      *   *    *    *          \033[30m"
	echo  "\033[31m       ****   *****    *    *          \033[30m"
	echo  "\033[31m       *      *   *    *    *          \033[30m"
	echo  "\033[31m       *      *   *  *****  ****       \033[30m"
	echo  "\033[31m=======================================\033[30m"	
}
PassMessage()                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         
{
	echo  "\033[32m=======================================\033[30m"
	echo  "\033[32m       *****   ***   *****  *****      \033[30m"
	echo  "\033[32m       *   *  *   *  *      *          \033[30m"
	echo  "\033[32m       *****  *****  *****  *****      \033[30m"
	echo  "\033[32m       *      *   *      *      *      \033[30m"
	echo  "\033[32m       *      *   *  *****  *****      \033[30m"
	echo  "\033[32m=======================================\033[30m"
}

Network=`system_profiler SPUSBDataType | grep -c "Apple USB Ethernet Adapter"`
while [ $Network -eq 0 ]
do 
  echo "\033[31m Pls plug Network Cable \033[30m"
  sleep 1
  Network=`system_profiler SPUSBDataType | grep -c "Apple USB Ethernet Adapter"`
done  
static-ip-address -timeout 10
if [ $? -eq 1 ];then 
FailMessage
echo ; echo "\033[31m Pls Check Network Connect ! \033[30m" ; echo 
exit 0
fi
/TE_Support/Scripts/Test_Process/serverIPConnection.sh
if [ $? -eq 1 ];then 
FailMessage
echo "\033[31m Can not connect with PDCA , Pls Check connect ... \033[30m" ; echo 
exit 0
fi 
PassMessage