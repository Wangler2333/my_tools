#!/bin/sh

Path="/Users/saseny/Desktop/PGQ_RR_5-11.17.0G2.dmg"           ## Bundle Path
FailMessage()
{
	echo  "\033[31m=======================================\033[30m"
	echo  "\033[31m       *****   ***   *****  *          \033[30m"
	echo  "\033[31m       *      *   *    *    *          \033[30m"
	echo  "\033[31m       ****   *****    *    *          \033[30m"
	echo  "\033[31m       *      *   *    *    *          \033[30m"
	echo  "\033[31m       *      *   *  *****  ****       \033[30m"
	echo  "\033[31m=======================================\033[30m"	
	exit 1
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
	exit 0
}
Return()
{
  if [ $? -eq 0 ];then 
     echo "\033[32m[PASS]\033[30m"
  else
     echo "\033[31m[FAIL]\033[30m" ; exit 1
  fi
} 
echo "\033[32m (1). Check External Disk Present ... \033[30m"  
if [ `diskutil list | grep -c "external"` -eq 0 ];then 
  echo "\033[31m [FAIL] No External Disk Presented !!! Pls Check it... \033[30m" ; exit 1
fi  
  Return
       
echo "\033[32m (2). Formatted Diskette ! \033[30m" 
  sudo diskutil eraseVolume JHFS+ UntitledHFS disk1s2    ## disk1s2 
  Return

echo "\033[32m (3). Restore Bundle ! \033[30m"
  sudo /usr/sbin/asr -s $Path -t /dev/disk1s2 -erase -noprompt
  Return

echo "\033[32m (4). Rename External Disk ! \033[30m"
  diskutil rename disk1s2 Download
  Return

if [ `ls /Volumes/MaxDisk | grep -c "start_phoenix_configuration.plist"` -ne 0 ];then 
  echo "\033[32m (5). Move Start Phonie_File ! \033[30m"
  mv /Volumes/MaxDisk/start_phoenix_configuration.plist /Volumes/MaxDisk/Phoenix
fi  

if [ $? -eq 0 ];then 
  PassMessage
else
  FailMessage
fi