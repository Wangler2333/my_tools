#!/bin/sh
#

SearchDir="/Users/phoenixmeng/Desktop/J45Ag"
TargetDir="$SearchDir/DOE"
TmpDir="$SearchDir/temp"
ResultFile="$SearchDir/DOE/Result.txt"

TargetDirChipset361="$TargetDir/Chipset361_PCIE"


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
	#	NewFolderName=`echo $i | sed 's/.*\///g' | sed 's/_.*//g'`
	#	NewFolderName=`echo $i | awk -F '/' '{print$NF}' | awk -F '.' '{print$1}' | awk -F '_' '{print$3}'`
	
		FolderName=`echo $i | awk -F '/' '{print$NF}' | awk -F '.' '{print$1}' | sed 's/.*EVT_//'`
		tempName=`echo $FolderName | sed 's/_PRE_FAIL_/_/' | sed 's/_PRE_PASS_/_/' | sed 's/_POST_FAIL_/_/' | sed 's/_POST_PASS_/_/'`
		
		NewFolderName=$tempName	
		Sernum=`echo $NewFolderName | sed 's/_.*//'`
		
		mkdir $TargetDirChipset361/$NewFolderName

    	tar -xzf $i

		#cp -rf /$TmpDir/$FolderName/_INDY_LOG_/Chipset/*361*.txt /$TargetDirChipset361/$NewFolderName
		
		for j in `find /$TmpDir/$FolderName/_INDY_LOG_/ -type f -name *361*.txt`;do
		#echo `cat $j`
		read=`cat $j | grep "PCIE	PCH	 4"`
		echo "$Sernum	$read" >> $ResultFile
		done
		
		sudo rm -rf /$TmpDir/$FolderName
	done
	sudo rm -rf /$TmpDir
	exit 0
else
exit 1
fi


