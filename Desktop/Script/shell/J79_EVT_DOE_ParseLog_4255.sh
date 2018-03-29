#!/bin/sh

SearchDir=`dirname $0`
TargetDir="$SearchDir/DOE"
TmpDir="$SearchDir/temp"
Project="J79_EVT"

copyflag=1

TargetDirSOCDRAM=$TargetDir/$Project"_SOCDRAM"

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

	mkdir $TargetDirSOCDRAM
	
else
	echo "Not found folder"
	exit 1
fi
}

createSubFolder()
{
		mkdir $TargetDirSOCDRAM/$NewFolderName
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
	
#*******************************
#			TIM DOE
#*******************************
ThermalInterfaceTest()
{

if [ ! -f $TargetDirTIM/ThermalInterface_Cpu.csv ];then
	touch $TargetDirTIM/ThermalInterface_Cpu.csv	
else

	if [ ! -s $TargetDirTIM/ThermalInterface_Cpu.csv ];then
	cat /$TmpDir/$FolderName/_APPLEINTERNAL_DIAGNOSTICS_LOGS/Logs/*Thermal_Interface_Cpu* | awk 'NR>1' >> $TargetDirTIM/ThermalInterface_Cpu.csv
	else
	cat /$TmpDir/$FolderName/_APPLEINTERNAL_DIAGNOSTICS_LOGS/Logs/*Thermal_Interface_Cpu* | awk 'NR>2' >> $TargetDirTIM/ThermalInterface_Cpu.csv
	fi
fi

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

GetSensorGroupKey()
{
	while read line
	do		
	case $line in
	*"Limit with Idle Test"* ) 
	getsensor=1
	unset SensorKey
	unset SersorRead
	ResultFile="SensorGroup3116_Idle.csv"
	;;
	*"Limit with Core Load Test"* ) 
	getsensor=1
	unset SensorKey
	unset SersorRead
	ResultFile="SensorGroup3105_CoreLoad.csv"
	;;
	*"Limit with Memory Load Test"* ) 
	getsensor=1
	unset SensorKey
	unset SersorRead
	ResultFile="SensorGroup3112_MemLoad.csv"
	;;
	*"Limit with System Load Test"* ) 
	getsensor=1
	unset SensorKey
	unset SersorRead
	ResultFile="SensorGroup3117_SystemLoad.csv"
	;;	
	*"XDBG\",TEXT=\"For"* )
	if [ "$getsensor" == 1 ];then
		if [ ! -s $TargetDir/$ResultFile ];then
		SensorKey=("${SensorKey[@]}" `echo $line | sed 's/low limit.*//' | awk -F 'For ' '{print$NF}'`)
		fi
		
		#echo $line | sed 's/.*value //' | sed 's/."//'
		#sleep 0.1
		
		SersorRead=("${SersorRead[@]}" `echo $line | sed 's/.*value //' | sed 's/."//' | sed 's/\,threadId=.*//g'`)
	fi
	;;
	*"TEST-TRST"* ) 
	if [ "$getsensor" == 1 ];then
		getsensor=0
	
	if [ ! -s $TargetDir/$ResultFile ];then
		echo "SerialNumber	${SensorKey[@]}" >> $TargetDir/$ResultFile
		Header=0
	fi
	
	echo "$SerialNumber	${SersorRead[@]}" >> $TargetDir/$ResultFile
	unset SensorKey
	unset SersorRead
	
	fi
	
	;;	
	esac
			
	done < $TargetDir/Temp.txt
	
	
}

SensorGroup()
{
if [ ! -f $TargetDir/temp.txt ];then
touch $TargetDir/temp.txt
fi

for n in `find $TmpDir/$FolderName -type f -maxdepth 8 -name processlog.plog -print`; do
	cat $n > $TargetDir/temp.txt
	GetSensorGroupKey	
done
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
		
		#TIM Test
		#ThermalInterfaceTest
			
		#Sensor
		#SensorGroup

		if [ "$copyflag" -eq 1 ];then

		#SOC DRAM, 4255
		cp -rf $TmpDir/$FolderName/_APPLEINTERNAL_DIAGNOSTICS_LOGS/Logs/SOC/*4255* $TargetDirSOCDRAM/$NewFolderName &>/dev/null

		fi
		
		sudo rm -rf /$TmpDir/$FolderName
	done
	
	IFS=$OLDIFS
	
	sudo rm -rf /$TmpDir
	sudo rm -rf /$TargetDir/temp.txt

removeEmpty
PrintFinal