#!/bin/ksh
##############################################################################
#  Filename: start_phoenix.sh.command
#
# SVN $Revision: 1665 $ $Date: 2009-07-09 13:56:37 +0800 (Thu, 09 Jul 2009) $
#
# Objective: A wrapper script to launch phoenix after sleeping for a defined
#            amount of time.  The PhoenixCE should never be called directly
#            from a login item.  This script should be called instead.
#
#
##############################################################################

touch /private/tmp/running

main()
{
	if [ ! -f "/Phoenix/Logs/ADPStatus.txt" ]; then
	echo "Unit first power on"
	ADPStatus=`/TE_Support/Scripts/Test_Process/ypc2 -rdk ACIN | awk '{print int($0)}'`
		if [ $ADPStatus -eq 0 ];then
			echo "Unit disconnected with Adapter"
			echo "${ADPStatus}" > "/Phoenix/Logs/ADPStatus.txt"
		else
			echo "Unit connected with Adapter"
			echo -e "\033[31m========================="
			echo -e "\033[31m*****   ***   *****  *   "
			echo -e "\033[31m*      *   *    *    *   "
			echo -e "\033[31m****   *****    *    *   "
			echo -e "\033[31m*      *   *    *    *   "
			echo -e "\033[31m*      *   *  *****  ****"
			echo -e "\033[31m========================="
			echo ""
			echo "按Y键关闭Unit[Y]:"
			
			read continue
			while [ $continue != Y ]; do
				echo "请输入Y然后手动重启电脑[Y]:"
				read continue;
			done
			if [ $continue == Y ]; then
				echo "Shut down unit......"
				shutdown -h now
				exit 1
			fi
		fi
	else
		echo "Unit has been powered on before"
	fi

	VERSION="1.0.14"
	echo "start_phoenix.sh.command version $VERSION"
	
	###############################################################################
	
	# if ALWAYSWAITING = 1, startup script waits until /Volumes/DIAG and /Volumes/MaxDisk are mounted before launching Phoenix.
	# if ALWAYSWAITING = 0, startup script waits until /Volumes/DIAG and /Volumes/MaxDisk are mounted or Until delay is completed before launching Phoenix.
	ALWAYSWAITING=1
	
	# This is a configurable delay (seconds) that is used to wait for the volume mounting.
	DELAY=55
	
	# This is a configurable delay (seconds) that is used for stabilizing the OS.
	#STABILIZE=3
        #workaround for Bluetooth mac address probing
	STABILIZE=20
	
	# How many EFI retries?
	MAX_EFI_RETRY=2
	
	# This is configurable that if it needs to call dump IO Registry before launching Phoenix
	# EXECUTE_IOREG_DUMP=1
	EXECUTE_KEXTSTAT=1
	
	# Phoenix processlog.plog location for logging 
	PHOENIX_LOG="/Phoenix/Logs/processlog.plog"
	###############################################################################
	
	COUNTER=0

	/Indy/Runtime_Files/OS/TestApps/DPCDParser.app/Contents/MacOS/DPCDParser -i i2c-over-aux -a 0x210 -l 7 >> /Phoenix/Logs/displayBERlog.txt
	
	if [ $ALWAYSWAITING -eq 1 ]; then
		echo "Always Waiting for /Volumes/DIAG and /Volumes/MaxDisk to be mounted"
	fi
	
	# Getting the partition information
	
	bootPartition=`df -l | grep ' /$' | awk '{print $1}'`
	
	echo "The   Boot partition is       $bootPartition"
	
	# Additional information regarding DIAG and Hidden Partition
	# In case it is needed in the future
	
	#bootSlice=${bootPartition##*s}
	#hiddenSlice=$((bootSlice-1))
	#hiddenPartition=${bootPartition%s*}s$hiddenSlice
	#retestSlice=$((bootSlice+1))
	#retestPartition=${bootPartition%s*}s$retestSlice
	#echo "Thus, the hidden partition is $hiddenPartition, and the hidden slice is [$hiddenSlice]"
	#echo "And,  the DIAG partition is   $retestPartition, and the DIAG slice is [$retestSlice]"
	
	# Getting information regarding MaxDisk volume.
	
	MaxDisk=`diskutil list | grep -c 'MaxDisk'`
	
	if [ $MaxDisk -ne 0 ]; then
		echo "Boot Volume name is already MaxDisk"
	else
		echo "Boot Volume name is not MaxDisk"
		echo "Renaming the boot volume to MaxDisk"
		diskutil rename $bootPartition MaxDisk
	fi 
	
	sleep 1
	
	
	if [ $ALWAYSWAITING -eq 1 ]; then 
		while ([ ! -d /Volumes/DIAG ]  || [ ! -d /Volumes/MaxDisk ])
		do
			echo "Waiting for MaxDisk and DIAG volume to be mounted.  No delay"
			echo "Press CTRL C to stop the launching process."
			sleep 20
			echo ""
		done	
	else
		while ([ $COUNTER -le $DELAY ] && ([ ! -d /Volumes/DIAG ] || [ ! -d /Volumes/MaxDisk ])) 
		do
			PERIOD=$((DELAY-COUNTER)) 
			echo "Waiting for MaxDisk and DIAG volume to be mounted... or Waiting for $PERIOD seconds."
			echo "Press CTRL C to stop the launching process."
			echo ""
			sleep 1
			COUNTER=$((COUNTER+1))
		done
	fi
	
	echo "Waiting for $STABILIZE secs to stabilize OS"
	sleep $STABILIZE
	
	# EFI retry stuff
	if [ -f "/Volumes/MaxDisk/efi_test.def" ]; then
		# ok we were supposed to run EFI 
		# but did we?
		if [ -f "/Volumes/DIAG/efi_cnsl.log" ]; then
			# it did run do nothing here.
			#remove the retrycount file if it is there.
			#rm /Volumes/DIAG/efi_rtry.cnt	#Removed for global life of the UUT retry count.
			echo ""
		else
			# how many retries do we have? 
			if [ -f "/Volumes/DIAG/efi_rtry.cnt" ]; then
				# get the number of retries already performed
				#EFI_RETRY_CNT=`cat /Volumes/DIAG/efi_rtry.cnt`
				EFI_RETRY_CNT=`cat /Volumes/DIAG/efi_rtry.cnt | wc -l`
			else
				EFI_RETRY_CNT=0
			fi
			
			# are we going to retry?
			if [ $EFI_RETRY_CNT -lt $MAX_EFI_RETRY ]; then
				# we need to increment the retry count.
				#echo "$((EFI_RETRY_CNT+1))" > /Volumes/DIAG/efi_rtry.cnt
				echo "$((EFI_RETRY_CNT+1)) "`date "+%m-%d-%C%y %H:%M:%S"` >> /Volumes/DIAG/efi_rtry.cnt
				echo "We are going to Retry EFI again.  It did not run last time."
				log_indy_message "CMMD-CSTT\",ProcessName=\"EXTRNL:start_phoenix.sh" "EFI Retry" $PHOENIX_LOG
				log_indy_message "PHNX-RTRY" "Retrying EFI [$((EFI_RETRY_CNT+1))/$MAX_EFI_RETRY]" $PHOENIX_LOG
				log_indy_message "CMMD-CRST\",ProcessName=\"EXTRNL:start_phoenix.sh" "EFI Retry" $PHOENIX_LOG
				# bless to go to EFI
				log_indy_message "CMMD-CSTT\",ProcessName=\"EXTRNL:start_phoenix.sh" "Launching /Phoenix/Tools/EFITool -b" $PHOENIX_LOG
				/Phoenix/Tools/EFITool -r
				log_indy_message "CMMD-CRST\",ProcessName=\"EXTRNL:start_phoenix.sh" "Launching /Phoenix/Tools/EFITool -b" $PHOENIX_LOG
				sleep 3
				echo "reboot"
				reboot
			else
				# not going to retry anymore.
				# continue on
				echo "EFI retries exceeded.  Continue on with testing"
				log_indy_message "PHNX" "EFI retries exceeded or no retires.  Continue on with testing" $PHOENIX_LOG
				#remove the retrycount file if it is there.
				#if [ -f "/Volumes/DIAG/efi_rtry.cnt" ]; then
				#	rm /Volumes/DIAG/efi_rtry.cnt		#Removed for global life of the UUT retry count.
				#fi
			fi
		fi
	fi

	
	# Generate ioreg dump...
# 	if [ EXECUTE_IOREG_DUMP -eq 1 ]; then
# 		echo "Executing ioreg -l"
# 		date +'==ioreg -l %Y/%m/%d %H:%M:%S==' >> /Phoenix/Logs/ioreg.log
# 		/usr/sbin/ioreg -l >> /Phoenix/Logs/ioreg.log
# 	fi
	

	# Generate kextstat...
	if [ EXECUTE_KEXTSTAT -eq 1 ]; then
		echo "Executing kextstat"
		date +'==kextstat %Y/%m/%d %H:%M:%S==' >> /Phoenix/Logs/kextstat.log
		/usr/sbin/kextstat >> /Phoenix/Logs/kextstat.log
	fi


	# make sure date is not 2001 on first start of phoenix
	if [ `date "+%Y"` -eq 2001 -a ! -e /Phoenix/Logs/state.txt ];
	then
		echo "Set date to 01/01/2009"
   		date 010108002009
	fi
	
	# check that if /Volumes/DIAG is found that create a link
	# this is to support test iteration count feature
	if [ -d "/Volumes/DIAG/Phoenix/Logs" ]; 
	then
		`/usr/bin/touch /Volumes/DIAG/Phoenix/Logs/TestIterationDB.txt`
		if ([ -f /Phoenix/Logs/TestIterationDB.txt ] && [ ! -L /Phoenix/Logs/TestIterationDB.txt ]); 
		then
			`cat /Phoenix/Logs/TestIterationDB.txt >> /Volumes/DIAG/Phoenix/Logs/TestIterationDB.txt`
			`rm -f /Phoenix/Logs/TestIterationDB.txt`
		fi
		`/bin/ln -s /Volumes/DIAG/Phoenix/Logs/TestIterationDB.txt /Phoenix/Logs/TestIterationDB.txt`
	fi
	
	# Launching PhoenixCE...
	cd /Indy
	echo "Launching Phoenix."
	echo "open PhoenixCE.app 2>&1 > /dev/console"
	open -a /Indy/PhoenixCE.app 2>&1 > /dev/console
	#PhoenixCE.app/Contents/MacOS/PhoenixCE 2>&1 > /dev/console
	
	killall Terminal &
	
	exit 0
}

# log_indy_message 
# takes in 3 of args
# arg 1 => message type
# arg 2 => text message
# arg 3 => logfile
log_indy_message()
{
	#context="0016cb7879fa",ts="2006/03/20 12:41:59",sid="PHNX",msg-type="PHNX-RTRY",TEXT="SomeText here"
	# get the context
	CONTEXT=`ifconfig en0 | grep ether | awk '{print $2}'`
	if [ "$CONTEXT" == "" ]; then
		CONTEXT="?"
	fi
	# get the timestamp
	TS=`date "+%C%y/%m/%d %H:%M:%S"`
	# get the msg-type
	# get the TEXT
	
	# build the string
	printf "context=\"$CONTEXT\",ts=\"$TS\",sid=\"PHNX_SCRP\",msg-type=\"$1\",TEXT=\"$2\"\n" >> $3

}

main $@
