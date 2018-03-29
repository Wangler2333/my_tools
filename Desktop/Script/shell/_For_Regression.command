#!/bin/sh

#  Script_For_Regression.sh
#  Swift_1
#
#  Created by Saseny on 2017/2/17.
#  Copyright © 2017年 Saseny. All rights reserved.

#************************************** Read Parameter **************************************************************************#

Dir=`dirname $0`
Date=`date +%Y_%m_%d_%H_%M_%S`
SerialNumber=`system_profiler SPHardwareDataType | grep "Serial Number" | sed 's/.*: //'`
Memory=`system_profiler SPHardwareDataType | grep "Memory" | sed 's/.*: //' | sed 's/ //g'`
Processor=`system_profiler SPHardwareDataType | grep "Processor Speed" | sed 's/.*: //' | sed 's/ //g'`
Storage=`system_profiler SPStorageDataType | grep "Capacity" | sed 's/.*: //' | sed 's/ //g' | head -1 | awk -F '.' '{print$1}'`

#************************************** Check Serial Number *********************************************************************#

SN_Check()
{
  if [ $SerialNumber != " " ];then
     SerialNumber=`cat < /Phoenix/Logs/SerialNumber.txt`
   else
     echo "There was no System Serial Number and '/Phoenix/Logs/SerialNumber.txt' Exist." ; exit 1
  fi
}

#************************************** Check Storage ***************************************************************************#

Check_Storage()
{
  if [ $Storage > "900" ];then
     Storage="1024GB"
  elif [ $Storage > "450" ];then
     Storage="512GB"
  else
     Storage="256GB"
  fi
}

#************************************** Read Units Message **********************************************************************#

Units_Message()
{
   Disc_Cat=`cat < /Volumes/DATA/_UnitsMessage/_regression_units_message.txt | grep -c "$SerialNumber"`
   if [ $Disc_Cat -eq 0 ];then
      echo "'/Volumes/DATA/_UnitsMessage/_regression_units_message.txt' no '$SerialNumber' Message. So need add it."
      echo "Pls insert Units number and Model Table number, Such as (45 993-13052):"
      read Units ModelTable
      echo "$Units;$SerialNumber;$ModelTable;$Processor|$Memory|$Storage" >> /Volumes/DATA/_UnitsMessage/_regression_units_message.txt
    else
      Units=`cat < /Volumes/DATA/_UnitsMessage/_regression_units_message.txt | grep "$SerialNumber" | awk -F ';' '{print$1}'`
      ModelTable=`cat < /Volumes/DATA/_UnitsMessage/_regression_units_message.txt | grep "$SerialNumber" | awk -F ';' '{print$3}'`
   fi
   WIP="$SerialNumber""+""$ModelTable"
}

#************************************** Touch Message on Desktop *****************************************************************#

Touch_Mesg()
{
   touch ~/Desktop/$Units
   touch ~/Desktop/$WIP
   touch ~/Desktop/694-05328-197
}

#************************************** Replace Table ****************************************************************************#

Table_replace()
{
   rm -rf /Phoenix/Table
   test -d /Volumes/DATA/_Table_regression/Tables
   if [ $? -eq 0 ];then
      cp -rf /Volumes/DATA/_Table_regression/Tables /Phoenix
      /TE_Support/Tools/Phoenix/cleanup_Phoenix2.command
    else
      echo "No Table in '/Volumes/DATA/_Table_regression'"
   fi
}

#************************************** Copy Test Log ****************************************************************************#

Copy_Log()
{
Check_tgz=`ls ~/Desktop | grep -c ".tgz"`
#Check_tgz=`find ~/Desktop -type f -iname *.tgz -print | wc -l | sed 's/.\ //g'`

    if [ $Check_tgz -eq 0 ];then
       open -a "/Applications/Utilities/Terminal.app" /TE_Support/Tools/Phoenix/COPYLOGS.pl
       sleep 15
    fi

    while [ $Check_tgz -eq 0 ]
    do
       echo "Waiting '/TE_Support/Tools/Phoenix/COPYLOGS.pl' running finish ...."
       sleep 3
       Check_tgz=`ls ~/Desktop | grep -c ".tgz"`
    done
    FileNeme="#""$Units""_"$SerialNumber
    mkdir -p ~/Desktop/$FileNeme ; sleep 1
    mv ~/Desktop/*.tgz ~/Desktop/$FileNeme &>/dev/null
    mv ~/Desktop/*.png ~/Desktop/$FileNeme &>/dev/null
    mv ~/Desktop/*.txt ~/Desktop/$FileNeme &>/dev/null
    mv ~/Desktop/*.csv ~/Desktop/$FileNeme &>/dev/null
    syslog >> ~/Desktop/$FileNeme/system.log

    cp -rf ~/Desktop/$FileNeme /Volumes/DATA/Log_For_Regression
}

#************************************** Unmount disk *****************************************************************************#

Unmount_disk()
{
   if [ ! -f /TE_Support/Tools/Phoenix/Unmount_Lunch.sh ];then
      cp -rf /Volumes/DATA/_Script/Unmount_Lunch.sh /TE_Support/Scripts/Test_Process
   fi
   open -a "/Applications/Utilities/Terminal.app" /TE_Support/Scripts/Test_Process/Unmount_Lunch.sh
}

#************************************** Start Phoenix ****************************************************************************#

Start_Phoenix()
{
   open -a "/Applications/Utilities/Terminal.app" /TE_Support/Scripts/Test_Process/start_command_c
}

#************************************** Restart & Shutdown ***********************************************************************#

ShutDown()
{
   sleep 3
   shutdown -h now
}

Restart()
{
   sleep 3
   reboot
}

#************************************** Some test Message out ********************************************************************#
# Serial Number , Date&Time , Test bundle , Custor bundle , Model Number

Some_Get()
{
    Date_time=`date +%Y/%m/%d@%T`

    case $1 in
    *1*)
      Test_bundle=`ls /Volumes/DATA/_Table_regression/Tables | grep ".tbproj3" | awk -F '.tbproj3' '{print$1}'`
      Statusd="Regression Run Start." ;;
    *2*)
      Test_bundle=`ls /Phoenix/Tables | grep ".tbproj3" | awk -F '.tbproj3' '{print$1}'`
      Statusd="Regression Run Finished." ;;
    esac

    Custor_bundle=`ls /*.dmg | awk -F '.dmg' '{print$1}'`
       if [ $Custor_bundle == " " ];then
    Custor_bundle="None"
    fi

    echo "$SerialNumber,$Date_time,$Test_bundle,$Custor_bundle,$ModelTable,$Statusd" >> /Volumes/DATA/_UnitsMessage/_regression_message.csv
}

#************************************** Main Script Start *****************************************************************************#

    echo "Start..."
    SN_Check
    Check_Storage
    Units_Message
    Touch_Mesg
    if [ -z $1 ];then
       echo "Pls inout number or String Such as [R/1 replace table] or [C/2 collect log]:"
       read Continue
    else
       Continue=$1
    fi
    case $Continue in
    *R*)
       Status="1"
       Table_replace
       Some_Get $Status
       ShutDown  ;;
    *C*)
       Status="2"
       Copy_Log
       Some_Get $Status
       Unmount_disk ;;
    *1*)
       Status="1"
       Table_replace
       Some_Get $Status
       ShutDown  ;;
    *2*)
       Status="2"
       Copy_Log
       Some_Get $Status
       Unmount_disk ;;
    *3*)
       Status="2"
       Copy_Log
       Some_Get $Status ;;
    esac

    echo "END..."

#************************************** Main Script End *****************************************************************************#
