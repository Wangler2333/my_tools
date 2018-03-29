#!/bin/sh
PathRoad="/Users/bundle/Desktop/J79_Bundle/_Command/_File" 

CheckBundleFilePath()
{
  if [ ! -f /Users/bundle/Desktop/J79_Bundle/_Command/_File/PathRoadFile.txt ] ;then
    echo "\033[31m Bundle File Pathroad not Exist. \033[30m" ; exit 1
  else
    TestBundlePath=`cat < $PathRoad/PathRoadFile.txt | sed -n '1p'`
    CMbundlePath=`cat < $PathRoad/PathRoadFile.txt | sed -n '2p'`
  fi 
}
CheckDefaultBundle()
{
  if [ ! -f /Users/bundle/Desktop/J79_Bundle/_Command/_File/DefaultBundle.txt ] ;then
    echo "\033[31m Default Bundle Name File not Exist. \033[30m" ; exit 1
  fi  
}    
DisplayDefault()
{
   echo "\033[34m"
   echo "Default Test Bundle Path: [`cat < $PathRoad/PathRoadFile.txt | sed -n '1p'`]"
   echo "Default CM Bundle Path: [`cat < $PathRoad/PathRoadFile.txt | sed -n '2p'`]"
   echo "Default Test Bundle Name: [`cat $PathRoad/DefaultBundle.txt | sed -n '1p'`]"
   echo "Default CM Bundle Name: [`cat $PathRoad/DefaultBundle.txt | sed -n '2p'`]" ; echo "\033[30m" ; exit 0
}   
  
failMessage()
{
	echo  "\033[31m========================="
	echo  "*****   ***   *****  *   "
	echo  "*      *   *    *    *   "
	echo  "****   *****    *    *   "
	echo  "*      *   *    *    *   "
	echo  "*      *   *  *****  ****"
	echo  "=========================\033[30m"	
	exit 1
}
dispplayResult()                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         
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
    echo "\033[31m" ; echo "'-a' : Only download Test Bundle."
    echo "'-b' : Change Bundle File Pathroad."
    echo "'-c' : Download CM at the same time. Input TestBundleName[\$2] cmBundleName[\$3] or After run input."
    echo "'-d' : Change Default Test & CM Bundle Name."
    echo "'-e' : Display Default Message."
    echo "'-h' : Display Help message." ; echo "\033[30m" ; exit 1
}  
doInitalize()
{
	echo "0. Unmount disk2"
	sleep 3
	diskutil unmountDisk /dev/disk1
	diskutil unmountDisk /dev/disk2

	#echo "1. Initalize disk0"
	checkDisk=`diskutil list | grep disk2 | grep -c MaxDisk`
	if [ $checkDisk != 1 ]; then
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
 		echo "\033[31m      #         #      #######   #         #                #        ##     #                  "
		echo ""
		echo "\033[31m是否要继续[Y/N]:"

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
	
	echo "1. Initalize disk2"
	sudo diskutil partitionDisk /dev/disk2 1 GPTFormat HFS+ Diagnostics 1G
	 
	echo "2. Setting up Test partition"
	#/usr/sbin/asr -partition /dev/disk0 -testsize 20g -retestsize 1g
    sudo /usr/sbin/asr -partition /dev/disk2 -testsize 70g -retestsize 1g -recoverysize 80g
    #sleep 5
    #sudo diskutil resizeVolume disk1s3 70G %5361644d-6163-11AA-AA11-00306543ECAC% KernelCore 1g	
}
restoreTEST()
{
	echo "3. Download to Test partition \033[32m "$TestBundle" \033[30m"
	sleep 3
	diskutil unmountDisk /dev/disk0s3
	sleep 3
	
    sudo /usr/sbin/asr -s $TestBundlePath/$TestBundle -t /dev/disk2s3 -erase -noprompt

	if [ "$?" != 0 ]; then
		failMessage
	fi
}
restoreCM()
{
	echo "5. Download to CM partition \033[32m "$cmBundle" \033[30m "
	
#	/Utilities/asr -s /Configurations/"$CM".dmg -t /dev/disk0s9 -hidden
	ditto -rsrcFork $CMbundlePath/$cmBundle /Volumes/MaxDisk
#	cp /2Z694-9444.dmg /dev/disk0s3
	if [ "$?" != 0 ]; then
		failMessage
	fi
}
  
starTime=`date +%s`


case $1 in 
*-a*)
   if [ ! -z $2 ]; then 
      echo "Pls input Test Bundle Name you need download."
      read TestBundle 
   fi 
   CheckBundleFilePath 
   doInitalize 
   restoreTEST ;;
*-b*)
   echo "\033[34mPls input Test Bundle Path Road:"
   read Test
   echo $Test > $PathRoad/PathRoadFile.txt
   echo "Pls input CM Bundle Path Road:"
   read CM
   echo $CM >> $PathRoad/PathRoadFile.txt
   echo "Changed! \033[30m" ; exit 0 ;;  
*-c*)
   if [ -z $2 ]; then  
      CheckDefaultBundle   
      A=`cat $PathRoad/DefaultBundle.txt | sed -n '1p'`
      echo "\033[34m Default Test Bundle Name is: $A.\033[30m" 
      TestBundle=$A.dmg
   else 
      TestBundle=$2.dmg   
   fi
   if [ -z $3 ];then
      CheckDefaultBundle
      B=`cat $PathRoad/DefaultBundle.txt | sed -n '2p'`
      echo "\033[34m Default CM Bundle Name is: $B.\033[30m" 
      cmBundle=$B.dmg
   else
      cmBundle=$3.dmg   
   fi
   CheckBundleFilePath
   doInitalize 
   restoreTEST
   restoreCM ;;
*-d*)
   echo "\033[34mPls input Test Bundle Name:"
   read Test
   echo $Test > $PathRoad/DefaultBundle.txt
   echo "Pls input CM Bundle Name:"
   read CM
   echo $CM >> $PathRoad/DefaultBundle.txt
   echo "Changed! \033[30m" ; exit 0 ;;
*-e*)
   DisplayDefault ;;        
*-h*)
   ScriptMessage ;;
*)
   ScriptMessage ;;   
esac

# diskutil renameVolume / Download
# rm /private/var/vm/swapfile*

    endTime=`date +%s`
    useTimeSample=`expr ${endTime} - ${starTime}`
    B=60
    timeleft=`echo "scale=2;$useTimeSample/$B" |bc` ; echo 
    echo "\033[34m [UsedTime: $timeleft min] \033[30m" ; echo ; dispplayResult