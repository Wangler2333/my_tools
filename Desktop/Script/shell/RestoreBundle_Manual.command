#!/bin/sh

Path="/private/var/root/Desktop/PGQ_RR_5-11.17.0G2.dmg"           ## Bundle Path
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


Manul()
{
echo "\033[35m -- Pls Confirm is it Restore now ? [ Continue (YES/Y/yes/y) or Stop (NO/N/no/n) ] .... \033[30m" 
read Input 
if [ $Input == "YES" ];then
echo " You Choose --[$Input] and Continue doing ! " ; echo ; Test
elif [ $Input == "Y" ];then
echo " You Choose --[$Input] and Continue doing ! " ; echo ; Test
elif [ $Input == "yes" ];then 
echo " You Choose --[$Input] and Continue doing ! " ; echo ; Test
elif [ $Input == "y" ];then 
echo " You Choose --[$Input] and Continue doing ! " ; echo ; Test
elif [ $Input == "NO" ];then 
echo " You Choose --[$Input] and Stoped ! " ; exit 1
elif [ $Input == "N" ];then
echo " You Choose --[$Input] and Stoped ! " ; exit 1
elif [ $Input == "no" ];then 
echo " You Choose --[$Input] and Stoped ! " ; exit 1
elif [ $Input == "n" ];then 
echo " You Choose --[$Input] and Stoped ! " ; exit 1
fi
echo "\033[31m Abnormal input volue , Pls check it .... \033[30m" ; exit 1
}

Test()
{
   echo "\033[34m (1). Check External Disk Present ... \033[30m"  

   if [ `diskutil list | grep -c "external"` -eq 0 ];then 
     echo "\033[31m [FAIL] No External Disk Presented !!! Pls Check it... \033[30m" ; exit 1
   fi  
     Return
       
   echo "\033[34m (2). Formatted Diskette ! \033[30m" 
     sudo diskutil eraseVolume JHFS+ UntitledHFS disk1s2    ## disk1s2 
     Return

   echo "\033[34m (3). Restore Bundle ! \033[30m"
     sudo /usr/sbin/asr -s $Path -t /dev/disk1s2 -erase -noprompt
     Return
 
   echo "\033[34m (4). Rename External Disk ! \033[30m"
     diskutil rename disk1s2 Download
     Return

   if [ `ls /Volumes/Download | grep -c "start_phoenix_configuration.plist"` -ne 0 ];then 
     echo "\033[34m (5). Move Start Phonie_File ! \033[30m"
     mv /Volumes/Download/start_phoenix_configuration.plist /Volumes/Download/Phoenix
   fi  
     Return

   echo "\033[34m (6). Unmount Disk /Volumes/Download ! \033[30m"
     diskutil unmount /Volumes/Download

   if [ $? -eq 0 ];then 
     PassMessage
   else
     FailMessage
   fi
}

Manul