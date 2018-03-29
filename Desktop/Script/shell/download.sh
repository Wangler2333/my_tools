#!/bin/sh

SCRIPT_DIR=`dirname $0`
DefaultFilePath="/usr/local/DefaultFile.txt"
starTime=`date +%s`

ParameterMessage()
{
   TestBundleName=`cat $DefaultFilePath | grep "TestBundleName" | sed 's/.*: //'`
   CustomerBundleName=`cat $DefaultFilePath | grep "CustomerBundleName" | sed 's/.*: //'`
   TestBundlePathRoad=`cat $DefaultFilePath | grep "TestBundlePathRoad" | sed 's/.*: //'`
   CustomerBundlePathRoad=`cat $DefaultFilePath | grep "CustomerBundlePathRoad" | sed 's/.*: //'`
   Testsize=`cat $DefaultFilePath | grep "Testsize" | sed 's/.*: //'`
   Retestsize=`cat $DefaultFilePath | grep "Retestsize" | sed 's/.*: //'`
   Recoverysize=`cat $DefaultFilePath | grep "Recoverysize" | sed 's/.*: //'`
   Disk=`cat $DefaultFilePath | grep "Disk" | sed 's/.*: //'`
   CoreDump=`cat $DefaultFilePath | grep "CoreDump" | sed 's/.*: //'`
}   
CheckDefaultFile()
{
  if [ ! -f $DefaultFilePath ] ;then
    echo "\033[31m Default File not Exist. \033[30m" ; exit 1
  fi 
}
DisplayDefault()
{
   echo "\033[34mDefault Testsize: [ $Testsize]"
   echo "Default Retestsize: [$Retestsize]"
   echo "Default Recoverysize: [$Recoverysize]"
   echo "Default CoreDump: [$CoreDump]"
   echo "Default Disk: [$Disk]"
   echo "Default Test Bundle Path: [ $TestBundlePathRoad ]"
   echo "Default CM Bundle Path: [ $CustomerBundlePathRoad ]"
   echo "Default Test Bundle Name: [ $TestBundleName ]"
   echo "Default CM Bundle Name: [ $CustomerBundleName ]\033[30m" ; exit 0
}
failMessage()
{
	echo  "\033[31m========================="
	echo  " *****   ***   *****  *    "
	echo  " *      *   *    *    *    "
	echo  " ****   *****    *    *    "
	echo  " *      *   *    *    *    "
	echo  " *      *   *  *****  **** "
	echo  "=========================\033[30m"	
	exit 1
}
passMessage()
{
	echo  "\033[32m==================================================="
	echo  "           *****   ***   *****  *****              "
	echo  "           *   *  *   *  *      *                  "
	echo  "           *****  *****  *****  *****              "
	echo  "           *      *   *      *      *              "
	echo  "           *      *   *  *****  *****              "
	echo  "===================================================\033[30m"
    exit 0
}
ScriptMessage()
{
    echo "\033[31m'-a' : Only download Test Bundle."
    echo "'-b' : Download CM at the same time. Input TestBundleName[\$2] cmBundleName[\$3] or After run input."
    echo "'-c' : Modify Default File."
    echo "'-d' : Display Default Message."
    echo "'-e' : Modify download size set."
    echo "'-f' : Partition CoreDump (0 or 1)."
    echo "'-g' : Modify Disk (disk1 or disk2)."
    echo "'-h' : Display Help message.\033[30m" ; exit 0
}   
displayMsg()
{
        echo "\033[31m            #      #######                  #            #                  #       #     #    "
		echo "\033[31m##############     #     #      #           #   #        # #   ###### ########    ##########  "
 		echo "\033[31m       #           #     #       ## #####   #    #       #  #     #      #        #       #    "
 		echo "\033[31m       #           #######        # #   # # #    #       #        #      #        #  #    #    "
 		echo "\033[31m      #            #     #     #    # # # # #      ###########   #    #######     #   #   #    "
 		echo "\033[31m      #            #     #      ##  # # # # #            #       #    #  #  #  ############### "
 		echo "\033[31m     ## #          #######       #  # # # # #  ###       #      ##### #  #  #     #       #    "
 		echo "\033[31m    # #  #                  #      ## # # # #    #  ######     # #  # #######     #  #    #    "
 		echo "\033[31m   #  #   ##   ###############    # # # # # #    #    #  #       #  # #  #  #    #    # # #    "
 		echo "\033[31m  #   #    ##         #           # # # # # #    #    #  #       #  # #  #  #   #        #     "
 		echo "\033[31m #    #     #      #  #  #      ##  # # # # #    #    #  #       #  # #######    ###########   "
 		echo "\033[31m#     #            #  #####      #    #     #    #    #   #      #  #    #       #  #   #  #   "
 		echo "\033[31m      #            #  #          #   # #    #    # #  ### #  #   #### ## #       #  #   #  #   "
 		echo "\033[31m      #           # # #          #  #   #   #    ## ###    # #   #  #   ##       #  #   #  #   "
 		echo "\033[31m      #          #   ##          # #    # # #    #   #     # #         #  #### ############### "
 		echo "\033[31m      #         #      #######   #         #                #        ##     #                  \033[30m"
}
doInitalize()
{
	echo "0. Unmount $Disk"
	sleep 3
	diskutil unmountDisk /dev/disk1
	diskutil unmountDisk /dev/$Disk

	#echo "1. Initalize disk0"
	checkDisk=`diskutil list | grep "$Disk" | grep -c MaxDisk`
	if [ $checkDisk != 1 ]; then
        displayMsg
		echo "\033[31m是否要继续[Y/N]:\033[30m"
		read -e continue
		while [ $continue != Y ] && [ $continue != N ]; do
			echo "\033[31m不是测试硬盘，是否要继续[Y/N]:\033[30m"
			read -e continue;
		done
		if [ $continue != Y ]; then
			echo "Stop...."
			exit
		fi
	fi
	echo "Continue...."
	sleep 3
	
	echo "1. Initalize $Disk"
	sudo diskutil partitionDisk /dev/$Disk 1 GPTFormat HFS+ Diagnostics 1G
	 
	echo "2. Setting up Test partition"
    sudo /usr/sbin/asr -partition /dev/$Disk -testsize $Testsize -retestsize $Retestsize -recoverysize $Recoverysize
    if [ $CoreDump -eq 1 ];then
      sleep 5
      DISKA="$Disk""s3"
      sudo diskutil resizeVolume $DISKA $Testsize %5361644d-6163-11AA-AA11-00306543ECAC% KernelCore 1g	
    fi
}
restoreTEST()
{
	echo "3. Download to Test partition \033[32m "$TestBundleName" \033[30m"
	sleep 3
	DISKB="$Disk""s3"
	diskutil unmountDisk /dev/$DISKB
	sleep 3	
    sudo /usr/sbin/asr -s $TestBundlePathRoad/$TestBundleName -t /dev/$DISKB -erase -noprompt
	if [ "$?" != 0 ]; then
		failMessage
	fi
}
restoreCM()
{
    DISKC="$Disk""s3"
    diskutil mountDisk /dev/$DISKC
	echo "5. Download to CM partition \033[32m "$CustomerBundleName" \033[30m "	
	ditto -rsrcFork $CustomerBundlePathRoad/$CustomerBundleName /Volumes/MaxDisk
	if [ "$?" != 0 ]; then
		failMessage
	fi
}

ModifyTestPath()
{
   echo "Pls input new DefaultPath_TestBundle"
   read NewTestPath
   sudo sed -i "" '/TestBundlePathRoad/d' $DefaultFilePath
   echo "TestBundlePathRoad: $NewTestPath" >> $DefaultFilePath
}   
ModifycmPath()
{
   echo "Pls input new DefaultPath_cmBundle"
   read NewCMPath
   sudo sed -i "" '/CustomerBundlePathRoad/d' $DefaultFilePath
   echo "CustomerBundlePathRoad: $NewCMPath" >> $DefaultFilePath
} 
ModifyTestBundleName()
{
   echo "Pls input new DefaultBundleName_TestBundle (.dmg)" 
   read NewTestBundleName
   sudo sed -i "" '/TestBundleName/d' $DefaultFilePath
   echo "TestBundleName: $NewTestBundleName" >> $DefaultFilePath
}
ModifycmBundleName()
{   
   echo "Pls input new DefaultBundleName_cmBundle (.dmg)" 
   read NewCMBundleName
   sudo sed -i "" '/CustomerBundleName/d' $DefaultFilePath
   echo "CustomerBundleName: $NewCMBundleName" >> $DefaultFilePath
}    
ModifyDefaultFile()
{
   echo "\033[31m Start Modify Default File..."
   echo "Pls input which you need Modify ?" ; echo " 'a': (Test Bundle Path)" ; echo " 'b': (CM Bundle Path)" ; echo " 'c': (Test Bundle Name)" ; echo " 'd': (CM Bundle Name)" ; echo " 'e': (Test & CM Bundle Path)" ; echo " 'f': (Test & CM Bundle Name)" ; echo " 'g': (Modify All)"
   read choose
   case $choose in 
   *a*)
     ModifyTestPath ;;
   *b*)
     ModifycmPath ;;
   *c*)
     ModifyTestBundleName ;;
   *d*)
     ModifycmBundleName ;;
   *e*)
     ModifyTestPath
     ModifycmPath ;;
   *f*)
     ModifyTestBundleName
     ModifycmBundleName ;;
   *g*)
     ModifyTestPath 
     ModifycmPath
     ModifyTestBundleName
     ModifycmBundleName ;;  
   *)
   echo "Wrong input!" ;;
   esac
   echo "\033[30m" ; exit 0
} 
ModifySize()
{   
   echo "Which Size you need modify. 1 (Test) 2 (Retest) 3 (Recovery)"
   read choose
   case $choose in 
   *1*)
     echo "Pls input new test size for testSize (70g)" 
     read NewTestSize
     sudo sed -i "" '/Testsize/d' $DefaultFilePath
     echo "Testsize: $NewTestSize" >> $DefaultFilePath ;;
   *2*)
     echo "Pls input new retest size for testSize (1g)" 
     read NewRetestSize
     sudo sed -i "" '/Retestsize/d' $DefaultFilePath
     echo "Retestsize: $NewRetestSize" >> $DefaultFilePath ;;  
   *3*)
     echo "Pls input new recovery size for testSize (1g)" 
     read NewRecoverySize
     sudo sed -i "" '/Recoverysize/d' $DefaultFilePath
     echo "Recoverysize: $NewRecoverySize" >> $DefaultFilePath ;;  
   *0*)
     echo "Pls input new test size for testSize (70g)" 
     read NewTestSize
     sudo sed -i "" '/Testsize/d' $DefaultFilePath
     echo "Testsize: $NewTestSize" >> $DefaultFilePath
     echo "Pls input new retest size for testSize (1g)" 
     read NewRetestSize
     sudo sed -i "" '/Retestsize/d' $DefaultFilePath
     echo "Retestsize: $NewRetestSize" >> $DefaultFilePath
     echo "Pls input new recovery size for testSize (1g)" 
     read NewRecoverySize
     sudo sed -i "" '/Recoverysize/d' $DefaultFilePath
     echo "Recoverysize: $NewRecoverySize" >> $DefaultFilePath ;;
    *)
     echo "Wrong Input!" ;;
   esac 
   exit 0           
}  
###### Main ######
case $1 in 
*-a*)
   CheckDefaultFile
   ParameterMessage
   if [ -z $2 ]; then     
      echo "\033[34m Default Test Bundle Name is: $TestBundleName.\033[30m" 
   else 
      TestBundleName=$2.dmg   
   fi 
   doInitalize 
   restoreTEST ;;   
*-b*)
   CheckDefaultFile
   ParameterMessage
   if [ -z $2 ]; then  
      echo "\033[34m Default Test Bundle Name is: $TestBundleName.\033[30m" 
   else 
      TestBundleName=$2.dmg   
   fi
   if [ -z $3 ];then
      CheckDefaultFile
      echo "\033[34m Default CM Bundle Name is: $CustomerBundleName.\033[30m" 
   else
      CustomerBundleName=$3.dmg   
   fi
   doInitalize 
   restoreTEST
   restoreCM ;;
*-c*) 
   CheckDefaultFile
   ParameterMessage
   ModifyDefaultFile ;;
*-d*)
   CheckDefaultFile
   ParameterMessage
   DisplayDefault ;;   
*-e*)
   CheckDefaultFile          ## Add new Modify Size
   ParameterMessage
   ModifySize ;; 
*-f*)
   CheckDefaultFile          ## Add partition Coredump 
   ParameterMessage
   echo "Are you need partition CoreDump? 0 or 1" 
   read choose
   sudo sed -i "" '/CoreDump/d' $DefaultFilePath
   echo "CoreDump: $choose" >> $DefaultFilePath 
   exit 0 ;;  
*-g*)
   CheckDefaultFile          ## Add Disk change 
   ParameterMessage
   echo "You Disk is ...? disk1 or disk2 or ..." 
   read choose
   sudo sed -i "" '/Disk/d' $DefaultFilePath
   echo "Disk: $choose" >> $DefaultFilePath 
   exit 0 ;;        
*-h*)
   CheckDefaultFile
   ParameterMessage
   ScriptMessage ;;
*)
   CheckDefaultFile
   ParameterMessage
   ScriptMessage ;;   
esac

# diskutil renameVolume / Download
# rm -rf /private/var/vm/swapfile*

endTime=`date +%s`
useTimeSample=`expr ${endTime} - ${starTime}`
B=60
timeleft=`echo "scale=2;$useTimeSample/$B" |bc` ; echo 
echo "\033[34m [UsedTime: $timeleft min] \033[30m" ; echo ; passMessage