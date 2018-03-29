#!/bin/sh
#set -x
##################### [PARAMETER] ##################################################
SystemSN=`system_profiler SPHardwareDataType | grep "Serial" | sed 's/.*: //'`
Number1=`nvram -p | grep -c "manufacturing-force-netboot"`
Number2=`nvram -p | grep -c "manufacturing-boot-on-attach"`
Time=`date +%y-%m-%d\ %H:%M:%S`
Info="[ModifyTime:$Time] [SystemSN: $SystemSN] [States(manufacturing-force-netboot):$Number1] [States(manufacturing-boot-on-attach):$Number2]"
Path="/Volumes/DATA/CheckNvramNand/"

Set_Nvram()
{
 sudo nvram manufacturing-force-netboot=%01
 sudo nvram manufacturing-boot-on-attach=%01
 rm -rf /Library/LaunchDaemons/com.apple.wabisabi.tester.plist
 rm -rf /AppleInternal/Wabi-Sabi/tester
 echo "\033[32m Set OK \033[30m" ; sleep 1 ; echo "\033[32m ShutDown Now !!! \033[30m" ; sleep 2
 shutdown -h now
}
Move_Log()
{ 
 mkdir -p $Path/Log/$SystemSN 
 cp -rf /Phoenix/Logs/ShutdownCause.txt $Path/Log/$SystemSN 
 cp -rf /Phoenix/Logs/processlog.plog $Path/Log/$SystemSN
 cp -rf /AppleInternal/Wabi-Sabi/tester $Path/Log/$SystemSN
 cp -rf /Library/LaunchDaemons/com.apple.wabisabi.tester.plist $Path/Log/$SystemSN
 nvram -p > $Path/Log/$SystemSN/Nvram.log
}
########################### [MAIN SCRIPT] ##########################################
[ ! -f /Volumes/DATA/CheckNvramNand ] && mkdir /Volumes/DATA/CheckNvramNand

 if [ $Number1 -eq 1 ];then 
   case $Number2 in  
   *1* )
   Move_Log
   echo $Info >> $Path/Message.log 
   echo "\033[31m boot-args All OK and Set again ! Pls Waiting ... \033[30m" ; Set_Nvram
   ;;
   *0* )
   Move_Log
   echo $Info >> $Path/Message.log 
   echo "\033[31m boot-args (manufacturing-boot-on-attach) Not OK and Set again ! Pls Waiting ... \033[30m" ; Set_Nvram 
   ;;
   esac
 else 
   Move_Log
   echo $Info >> $Path/Message.log 
   echo "\033[32m boot-args Not OK and Set again ! Pls Waiting ... \033[30m" ; Set_Nvram
 fi
####################################################################################