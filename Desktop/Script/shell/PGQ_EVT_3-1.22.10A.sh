#!/bin/sh

CM=694-03021-380
failMessage()
{
	echo  "\033[31m========================="
	echo  "\033[31m*****   ***   *****  *   "
	echo  "\033[31m*      *   *    *    *   "
	echo  "\033[31m****   *****    *    *   "
	echo  "\033[31m*      *   *    *    *   "
	echo  "\033[31m*      *   *  *****  ****"
	echo  "\033[31m========================="
	
	exit
}

doInitalize()
{
	echo "0. Unmount disk0"
	sleep 3
	diskutil unmountDisk /dev/disk1
	diskutil unmountDisk /dev/disk0

	#echo "1. Initalize disk0"
	checkDisk=`diskutil list | grep disk0 | grep -c MaxDisk`
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
			echo "\033[31m不是测试硬盘，是否要继续[Y/N]:"
			read -e continue;
		done
		if [ $continue != Y ]; then
			echo "\033[30mStop...."
			exit
		fi
	fi
	echo "\033[30mContinue...."
	sleep 3


	echo "1. Initalize disk0"
	diskutil partitionDisk /dev/disk0 1 GPTFormat HFS+ Diagnostics 1G
	 
	echo "2. Setting up Test partition"
	#/usr/sbin/asr -partition /dev/disk0 -testsize 20g -retestsize 1g
    /usr/sbin/asr -partition /dev/disk0 -testsize 80g -retestsize 5g -recoverysize 18g
    sudo diskutil resizeVolume disk0s3 80G %5361644d-6163-11AA-AA11-00306543ECAC% KernelCore 1g
	  

	
}


restoreTEST()
{
	echo "3. Download to Test partition "
	sleep 3
	diskutil unmountDisk /dev/disk0s3
	sleep 3

	
/usr/sbin/asr -s /Volumes/RUNIN_HDD/J79_4-1.0.0_0_2033.dmg -t /dev/disk0s3 -erase -noprompt

	if [ "$?" != 0 ]; then
		failMessage
	fi

}


restoreCM()
{
#	echo "5. Download to CM partition "$CM""
	
#	/Utilities/asr -s /Configurations/"$CM".dmg -t /dev/disk0s9 -hidden
#	ditto -rsrcFork /694-03021-380.dmg /Volumes/MaxDisk
#	cp /2Z694-9444.dmg /dev/disk0s3
	
	if [ "$?" != 0 ]; then
		failMessage
	fi

}
 
dispplayResult()                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         
{
	echo "6. Display Result"

	echo -e "\033[32m==================================================="
	echo -e "\033[32m           *****   ***   *****  *****              "
	echo -e "\033[32m           *   *  *   *  *      *                  "
	echo -e "\033[32m           *****  *****  *****  *****              "
	echo -e "\033[32m           *      *   *      *      *              "
	echo -e "\033[32m           *      *   *  *****  *****              "
	echo -e "\033[32m==================================================="

}

#______________________________________
# Wow, the main routine :-)
  diskutil renameVolume / Download
 # c=`sw_vers | grep BuildVersion | grep -c "12E3067"`

#	if [ $c -eq 0 ]; then
#	 echo "\033[31mBoot OS and TSD HDD is Wrong "
#	  failMessage
	   
		
#	fi
	
	#x=`diskutil list | grep -c "Macintosh HD"`

	#if [ $x -eq 0 ]; then
	#	failMessage
	#else

	#	y=`diskutil list | grep -c "DIAG"`

	#	if [ $y -eq 1 ]; then
		#	failMessage
	#	fi
	#fi
	
	rm /private/var/vm/swapfile*
	
	date
	
	doInitalize
	restoreTEST
	diskutil mountDisk /dev/disk0s3
	restoreCM
	sleep 2

	echo "Set pathing"
	#/usr/sbin/nvram boot-args=""
	sleep 3
	shutdown -h -o +0
	dispplayResult
	date
     