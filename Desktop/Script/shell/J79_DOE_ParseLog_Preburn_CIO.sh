#!/bin/sh

SearchDir=`dirname $0`
TargetDir="$SearchDir/DOE"
TmpDir="$SearchDir/temp"
Project="J79_EVT"

copyflag=1

TargetDirUSB10G=$TargetDir/$Project"_USB10G"
TargetDirTBT10G=$TargetDir/$Project"_TBT10G"
TargetDirTBT20G=$TargetDir/$Project"_TBT20G"

#**********Create folder_Start*********************
createDOEFolder()
{
if [ -d $SearchDir ]; then
	if [ ! -d $TmpDir ]; then
		mkdir $TmpDir
	fi
	
	if [ ! -d $TargetDir ]; then
		mkdir $TargetDir
	fi

	mkdir $TargetDirUSB10G
	mkdir $TargetDirTBT10G
	mkdir $TargetDirTBT20G
	
else
	echo "Not found folder"
	exit 1
fi
}

createSubFolder()
{		
		mkdir $TargetDirUSB10G/$NewFolderName
		mkdir $TargetDirTBT10G/$NewFolderName
		mkdir $TargetDirTBT20G/$NewFolderName
}


#*******************************
#	Remove Empty folder
#*******************************
removeEmpty()
{
cd $TargetDir
ls -1 > $TargetDir/zFolder.txt

while read line
do
	cd $TargetDir/$line
	
	ls -1 > $TargetDir/zSN.txt
	
	while read SN
	do
		if [ "$(ls -A $TargetDir/$line/$SN)" ];then
			echo "$TargetDir/$line/$SN: Found the file" >> $TargetDir/zResult.txt
	
		else
			echo "$TargetDir/$line/$SN: Nothing!!!!!" >> $TargetDir/zResult.txt
			rm -rf $TargetDir/$line/$SN
		fi
	done < $TargetDir/zSN.txt

done < $TargetDir/zFolder.txt

rm -rf $TargetDir/zSN.txt
rm -rf $TargetDir/zFolder.txt
rm -rf $TargetDir/zResult.txt

}	

#*****************************************************
#  			SensorParser
#*****************************************************

PrintFinal()
{
	echo -e "\033[32m===================================================\033[m"
	echo -e "\033[32m           ****   *****  *   *  *****              \033[m"
	echo -e "\033[32m           *   *  *   *  **  *  *                  \033[m"
	echo -e "\033[32m           *   *  *   *  * * *  *****              \033[m"
	echo -e "\033[32m           *   *  *   *  *  **  *                  \033[m"
	echo -e "\033[32m           ****   *****  *   *  *****              \033[m"
	echo -e "\033[32m===================================================\033[m"
	echo -e "\033[32mTotal Process [$TotalLog] Data						\033[m"
	echo -e "\033[32m===================================================\033[m"
}

#*****************************************************
#  			Main Script Start Here
#*****************************************************
#
# @ HT Law, 2 Feb 2014
#=====================================================
# 18 June:
# - Fix bug on calc the total log Process
# - Skip cat the T101 if summary csv not exist
# - Add handler for directory have space
#*****************************************************

createDOEFolder
TotalLog=0

OLDIFS=$IFS
IFS=$'\n'

cd $TmpDir
OverallLog=`find $SearchDir -type f -iname *.tgz -print | wc -l | sed 's/\ //g'`

    for i in `find $SearchDir -type f -iname *.tgz -print`; do      	
		TotalLog=`expr $TotalLog + 1`
		echo "Processing log [$TotalLog / $OverallLog]"
		
		#From Typical Log
		#**********************
		#SerialNumber=`echo $i | awk -F '/' '{print$NF}' | awk -F '.' '{print$1}' | awk -F '_' '{print$1}'`
		#FolderName=`echo $i | sed 's/.*\///g' | sed 's/.tgz//g'`
	
		#From Skynet Log (Have prefix Jxx)
		#**********************
		#SerialNumber=`echo $i | awk -F '/' '{print$NF}' | awk -F '.' '{print$1}' | awk -F '_' '{print$3}'`
		
		FolderName=`echo $i | awk -F '/' '{print$NF}' | awk -F '.' '{print$1}' | sed 's/.*C02/C02/'`
		SerialNumber=`echo $FolderName | awk -F '_' '{print$1}'`
		
		NewFolderName=$FolderName
		createSubFolder
		
    	tar -xzf $i &>/dev/null

		if [ "$copyflag" -eq 1 ];then

		#CIO 10G 20G
		cp -rf $TmpDir/$FolderName/_APPLEINTERNAL_DIAGNOSTICS_LOGS/Logs/TBTEyeLogs/*4507* $TargetDirUSB10G/$NewFolderName &>/dev/null
		cp -rf $TmpDir/$FolderName/_APPLEINTERNAL_DIAGNOSTICS_LOGS/Logs/TBTEyeLogs/*4508* $TargetDirUSB10G/$NewFolderName &>/dev/null
		cp -rf $TmpDir/$FolderName/_APPLEINTERNAL_DIAGNOSTICS_LOGS/Logs/TBTEyeLogs/*4194* $TargetDirTBT10G/$NewFolderName &>/dev/null
		cp -rf $TmpDir/$FolderName/_APPLEINTERNAL_DIAGNOSTICS_LOGS/Logs/TBTEyeLogs/*4195* $TargetDirTBT10G/$NewFolderName &>/dev/null
		cp -rf $TmpDir/$FolderName/_APPLEINTERNAL_DIAGNOSTICS_LOGS/Logs/TBTEyeLogs/*4384* $TargetDirTBT20G/$NewFolderName &>/dev/null
		cp -rf $TmpDir/$FolderName/_APPLEINTERNAL_DIAGNOSTICS_LOGS/Logs/TBTEyeLogs/*4385* $TargetDirTBT20G/$NewFolderName &>/dev/null

		fi
		
		sudo rm -rf /$TmpDir/$FolderName
	done
	
	IFS=$OLDIFS
	
	sudo rm -rf /$TmpDir
	sudo rm -rf /$TargetDir/temp.txt

removeEmpty
PrintFinal