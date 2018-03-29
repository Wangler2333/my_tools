#!/bin/sh
#

SearchDir="/private/var/root/Desktop/Pass"
TargetDir="$SearchDir/TM0P_Sensor"
TmpDir="$SearchDir/temp"
ResultFile="$SearchDir/TM0P_Sensor/Result.txt"

TargetDirTM0P="$TargetDir/TM0P_Sensor"


if [ -d $SearchDir ]; then

	if [ ! -d $TargetDir ]; then
		mkdir $TargetDir
		mkdir $TargetDirChipset361
		
	fi
	if [ ! -d $TmpDir ]; then
		mkdir $TmpDir
	fi
	cd $TmpDir
    for i in `find $SearchDir -type f -iname *.tgz -print`; do      
        FolderName=`echo $i | sed 's/.*\///g' | sed 's/.tgz//g'`
	
		FolderName=`echo $i | awk -F '/' '{print$NF}' | awk -F '.' '{print$1}' | sed 's/.*EVT_//'`
		tempName=`echo $FolderName | sed 's/_PRE_FAIL_/_/' | sed 's/_PRE_PASS_/_/' | sed 's/_POST_FAIL_/_/' | sed 's/_POST_PASS_/_/'`
		
		NewFolderName=$tempName	
		Sernum=`echo $NewFolderName | sed 's/_.*//'`
		
		mkdir $TargetDirTM0P_Sensor/$NewFolderName

    	tar -xzf $i
    	
    	plog="/$TmpDir/$FolderName/_PHOENIX_LOGS_PROCESSLOG.PLOG/processlog.plog"
    	
    	cat $plog | grep "TEXT-XVDG|TM0P" | > $ResultFile		

		done
		
		sudo rm -rf /$TmpDir/$FolderName
		
	sudo rm -rf /$TmpDir
	exit 0
else
exit 1
fi


