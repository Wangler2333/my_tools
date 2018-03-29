#!/bin/sh
# Developed by Ferris Feng.
# 12-26-2013 Initial release v1.0
# 12-30-2013 release 1.1.
	# Fix bug with "case in" and 
	# Fix incorrect output folder name "FQC4" for ROE station.
# 01-07-2014 release 1.2.
	# In version 1.1, every testers of LCD1 & LCD2 host permanently mount TIA server by afp protocol.
	# And it seems that there is a limitation for the number of simultaneous collection. Consequently some host would fail to mount TIA server.
	# Instead of permanently mounting TIA volumes, using ftp command to upload result file into TIA server.
	# TIA server changed to use IP 10.0.0.90 for LCD1 & LCD2 hosts accessing.
	# Leave some stations (e.g., CBTS and REIN) unchanged since only a few hosts accesses server.
# 01-07-2014 release 1.3 Ferris Feng.
	# J52 panel probed display info has different info and as a result display programmed SN can not be parsed successfully.
	# Change to use command "/Indy/Runtime_Files/OS/TestApps/PanelDetect.app/Contents/MacOS/PanelDetect -c" to get programmed display SN.
# 01-08-2014 release 1.4 Ferris Feng.
	# LCD2 output result file into correct folder
# 01-11-2014 release 1.5 Ferris Feng.
	# LCD2 output result file into correct folder
	# QSMC shop floor would rather to use unified ip 10.0.0.91 to capture txt files.
# 01-14-2014 release 1.6 Ferris Feng.
	# For ROE and REIN station, shopfloor logic still asks for pass/fail result to be in place. Modify script to accommodate it accordingly. 
# 02-27-2014 release 1.7 Ferris Feng.
	# For LCD3 station, do not parse programmed display SN from process.plog. Instead, use PanelDetect tool like LCD1. 
# 03-04-2014 release 1.8 Ferris Feng.
	# LCD2 process optimization - Do not connect camera cable hence no need to send out camera sn for SFIS to verify.
	# Note that J52 and J53 may have different stories.
# 03-19-2014 release 1.9 Phoenix Meng.
	# LCD2 add display SN in the txt file same as LCD1.
# 04-04-2014 release 1.10 Ferris Feng.
	# LL needs to send out fixture camera SN to control retest.
# 07-11-2014 release 1.11 Phoenix Meng.
	# Modify LCD2 when failed show "F" in the txt file instead of "p".

		
scriptVersion="1.11"
resultFlag=""
cleanRoom_SI_Report=""
stationFlag=""
timeStamp=`date "+%Y%m%d%H%M%S"`
outputFileName=""

if [ $# -eq 2 ]; then
	resultFlag="$1"
	stationFlag="$2"
else
	echo "Incoming argument is not correct."
	exit -3
fi


cbts_SNmatching()
{
	# Need to run mount_afp command to mount afp volumes first
	#if [ ! -d /Users/Shared/ResultTxt/sfs/ ]; then
	#	mount_afp afp://test:test@10.0.0.91/UnitID\ Folder/ /Users/Shared/ResultTxt
	#	sleep 5
	#fi

	#if [ ! -d "/Users/Shared/ResultTxt/sfs/CBTS" ]; then
	#	echo "/Users/Shared/ResultTxt/sfs/CBTS is not found"
	#	exit -11
	#fi

	if [ ! -f "/Phoenix/Logs/SerialNumber.txt" ]; then
		echo "/Phoenix/Logs/SerialNumber.txt is not found"
		exit -12
	else
		cleanRoom_SI_Report=`cat /Phoenix/Logs/SerialNumber.txt`
		outputFileName=`cat /Phoenix/Logs/SerialNumber.txt`
		outputFileName="${outputFileName}""CBTS.txt"
	fi
	
	if [ "${resultFlag}" == "pass" ]; then
		cleanRoom_SI_Report="${cleanRoom_SI_Report}"",""CBTS"",""${timeStamp}"",""P"","
	else	
		cleanRoom_SI_Report="${cleanRoom_SI_Report}"",""CBTS"",""${timeStamp}"",""F"","
	fi 
	
	if [ ! -f "/Phoenix/Logs/Camera_SerialNumber.txt" ]; then
		echo "cat /Phoenix/Logs/Camera_SerialNumber.txt is not found"
		exit -13
	else	
	    cameraSN=`cat /Phoenix/Logs/Camera_SerialNumber.txt`
	fi
		
	cleanRoom_SI_Report="${cleanRoom_SI_Report}""${cameraSN}"
		
	#Ferris echo "${cleanRoom_SI_Report}" > "/Users/Shared/ResultTxt/${outputFileName}"
	#echo "${cleanRoom_SI_Report}" > "/Users/Shared/ResultTxt/sfs/CBTS/${outputFileName}"
	#
	#if [ `echo $?` -ne 0 ]; then
	#	echo "Failed to output the result file"
	#	exit -14
	#fi
	echo "${cleanRoom_SI_Report}" > "/tmp/${outputFileName}"
	
	if [ `echo $?` -ne 0 ]; then
		echo "Failed to output the result file"
		exit -35
	fi
	
	# Now it's ready to ftp the file into TIA server with retry logic in place.
	# Ping check TIA server first.
	ping -c 2 10.0.0.91 >/dev/null 2>&1
	if [ `echo $?` -ne 0 ]
	then
		echo "Can not ping server 10.0.0.91."
		exit -36
	fi		 
	
	cd /tmp
	retryNumber=0
	waitTime=0
	while [ ${retryNumber} -lt 4 ]
	do 
		retryNumber=`expr ${retryNumber} + 1`
		waitTime=$((2**${retryNumber}))
		ftp -du ftp://test:test@10.0.0.91/%2F"UnitID Folder"/sfs/CBTS/ "${outputFileName}"
		# make sure ftp succeeded.
		if [ `echo $?` -ne 0 ]
		then
			echo "ftp command tries:<${retryNumber}>."
			sleep "${waitTime}"
		else
			break
		fi	
	done
	# Did we finally successfully upload file to ftp?
	if [ ${retryNumber} -eq 4 ]
	then
		echo "After 4x tries, ftp command still failed."
		exit -37
	fi
	
	# Delete result file
	rm -f "/tmp/${outputFileName}" 		

}


cbt_SNmatching()
{
	# Need to run mount_afp command to mount afp volumes first
	#if [ ! -d /Users/Shared/ResultTxt/sfs/ ]; then
	#	mount_afp afp://test:test@10.0.0.91/UnitID\ Folder/ /Users/Shared/ResultTxt
	#	sleep 5
	#fi

	#if [ ! -d "/Users/Shared/ResultTxt/sfs/CBTS" ]; then
	#	echo "/Users/Shared/ResultTxt/sfs/CBTS is not found"
	#	exit -11
	#fi

	if [ ! -f "/Phoenix/Logs/SerialNumber.txt" ]; then
		echo "/Phoenix/Logs/SerialNumber.txt is not found"
		exit -12
	else
		cleanRoom_SI_Report=`cat /Phoenix/Logs/SerialNumber.txt`
		outputFileName=`cat /Phoenix/Logs/SerialNumber.txt`
		outputFileName="${outputFileName}""CBT.txt"
	fi
	
	if [ "${resultFlag}" == "pass" ]; then
		cleanRoom_SI_Report="${cleanRoom_SI_Report}"",""CBT"",""${timeStamp}"",""P"","
	else	
		cleanRoom_SI_Report="${cleanRoom_SI_Report}"",""CBT"",""${timeStamp}"",""F"","
	fi 
	
	#if [ ! -f "/Phoenix/Logs/Camera_SerialNumber.txt" ]; then
	#	echo "cat /Phoenix/Logs/Camera_SerialNumber.txt is not found"
	#	exit -13
	#else	
	#    cameraSN=`cat /Phoenix/Logs/Camera_SerialNumber.txt`
	#fi
	
	if [ ! -f "/Indy/Logs/CameraSN.txt" ]; then
		echo "/Indy/Logs/CameraSN.txt is not found"
		exit -13
	else	
		cameraSN=`cat /Indy/Logs/CameraSN.txt | cut -d ":" -f 2 | awk '{print $1}'`
	fi
		
	cleanRoom_SI_Report="${cleanRoom_SI_Report}""${cameraSN}"
		
	#Ferris echo "${cleanRoom_SI_Report}" > "/Users/Shared/ResultTxt/${outputFileName}"
	#echo "${cleanRoom_SI_Report}" > "/Users/Shared/ResultTxt/sfs/CBTS/${outputFileName}"
	#
	#if [ `echo $?` -ne 0 ]; then
	#	echo "Failed to output the result file"
	#	exit -14
	#fi
	echo "${cleanRoom_SI_Report}" > "/tmp/${outputFileName}"
	
	if [ `echo $?` -ne 0 ]; then
		echo "Failed to output the result file"
		exit -35
	fi
	
	# Now it's ready to ftp the file into TIA server with retry logic in place.
	# Ping check TIA server first.
	ping -c 2 10.0.0.91 >/dev/null 2>&1
	if [ `echo $?` -ne 0 ]
	then
		echo "Can not ping server 10.0.0.91."
		exit -36
	fi		 
	
	cd /tmp
	retryNumber=0
	waitTime=0
	while [ ${retryNumber} -lt 4 ]
	do 
		retryNumber=`expr ${retryNumber} + 1`
		waitTime=$((2**${retryNumber}))
		ftp -du ftp://test:test@10.0.0.91/%2F"UnitID Folder"/sfs/CBT/ "${outputFileName}"
		# make sure ftp succeeded.
		if [ `echo $?` -ne 0 ]
		then
			echo "ftp command tries:<${retryNumber}>."
			sleep "${waitTime}"
		else
			break
		fi	
	done
	# Did we finally successfully upload file to ftp?
	if [ ${retryNumber} -eq 4 ]
	then
		echo "After 4x tries, ftp command still failed."
		exit -37
	fi
	
	# Delete result file
	rm -f "/tmp/${outputFileName}" 		

}
		

rein_SNmatching()
{
    # REIN needs to remove camera function test. So it expects pass/fail argument to be always "P"
	# Need to run mount_afp command to mount afp volumes first
	if [ ! -d /Users/Shared/ResultTxt/sfs/ ]; then
		mount_afp afp://test:test@10.0.0.91/UnitID\ Folder/ /Users/Shared/ResultTxt
		sleep 5
	fi

	if [ ! -d "/Users/Shared/ResultTxt/sfs/REIN" ]; then
		echo "/Users/Shared/ResultTxt/sfs/REIN is not found"
		exit -21
	fi

	if [ ! -f "/Phoenix/Logs/SerialNumber.txt" ]; then
		echo "/Phoenix/Logs/SerialNumber.txt is not found"
		exit -22
	else
		cleanRoom_SI_Report=`cat /Phoenix/Logs/SerialNumber.txt`
		outputFileName=`cat /Phoenix/Logs/SerialNumber.txt`
		outputFileName="${outputFileName}""REIN.txt"
	fi
	
	if [ "${resultFlag}" == "pass" ]; then
		cleanRoom_SI_Report="${cleanRoom_SI_Report}"",""REIN"",""${timeStamp}"",""P"","
	else	
		cleanRoom_SI_Report="${cleanRoom_SI_Report}"",""REIN"",""${timeStamp}"",""P"","
	fi 
	
	if [ ! -f "/Phoenix/Logs/processlog.plog" ]; then
		echo "/Phoenix/Logs/processlog.plog is not found"
		exit -13
	else	
		cameraSN=`cat /Phoenix/Logs/processlog.plog | grep -m 1 'type="Camera"' | sed 's/.*type="Camera".*serialNumber="\(.*\)" & firmwareVersion.*$/\1/'`
	fi
	
	cleanRoom_SI_Report="${cleanRoom_SI_Report}""${cameraSN}"
		
	echo "${cleanRoom_SI_Report}" > "/Users/Shared/ResultTxt/sfs/REIN/${outputFileName}"
	
	if [ `echo $?` -ne 0 ]; then
		echo "Failed to output the result file"
		exit -24
	fi
}

lcd1_SNmatching()
{
    # LCD1 equals FQC3
    # LCD1 does not connect camera cable to run test. So for this station, we need to caputure glass SN.
	# Need to run mount_afp command to mount afp volumes first
	
	#if [ ! -d /Users/Shared/ResultTxt/sfs/ ]; then
	#	mount_afp afp://test:test@10.0.0.91/UnitID\ Folder/ /Users/Shared/ResultTxt
	#	sleep 5
	#fi

	#if [ ! -d "/Users/Shared/ResultTxt/sfs/FQC3" ]; then
	#	echo "/Users/Shared/ResultTxt/sfs/FQC3 is not found"
	#	exit -31
	#fi

	if [ ! -f "/Phoenix/Logs/SerialNumber.txt" ]; then
		echo "/Phoenix/Logs/SerialNumber.txt is not found"
		exit -32
	else
		cleanRoom_SI_Report=`cat /Phoenix/Logs/SerialNumber.txt`
		outputFileName=`cat /Phoenix/Logs/SerialNumber.txt`
		outputFileName="${outputFileName}""FQC3.txt"
	fi
	
	if [ "${resultFlag}" == "pass" ]; then
		cleanRoom_SI_Report="${cleanRoom_SI_Report}"",""FQC3"",""${timeStamp}"",""P"","
	else	
		cleanRoom_SI_Report="${cleanRoom_SI_Report}"",""FQC3"",""${timeStamp}"",""F"","
	fi 

    # Verify process.plog file existence and read back programmed display SN
    if [ ! -f /Volumes/MaxDisk/Phoenix/Logs/processlog.plog ]; then
        echo "Did not see file /Volumes/MaxDisk/Phoenix/Logs/processlog.plog"
        exit -33
    fi
    # programmedDisplaySN=`cat /Volumes/MaxDisk/Phoenix/Logs/processlog.plog | grep -i 'class="display"' | cut -d , -f 28 | cut -d = -f 2 | cut -d \" -f 2`
    # See script v1.3 release note
    panelDetectOutput=`/TE_Support/Tools/LCD1/PanelDetect.app/Contents/MacOS/PanelDetect -c`
    programmedDisplaySN=`echo "${panelDetectOutput}" | grep -i 'Serial' | cut -d : -f 2 | sed 's/[[^ ]]*//g'`
    
    if [ `echo $?` -ne 0 ]; then
        echo "Errow with parsing programmed SN from processlog.plog."
        exit -34
    fi

	cleanRoom_SI_Report="${cleanRoom_SI_Report}""${programmedDisplaySN}"
		
	echo "${cleanRoom_SI_Report}" > "/tmp/${outputFileName}"
	
	if [ `echo $?` -ne 0 ]; then
		echo "Failed to output the result file"
		exit -35
	fi
	
	# Now it's ready to ftp the file into TIA server with retry logic in place.
	# Ping check TIA server first.
	ping -c 2 10.0.0.91 >/dev/null 2>&1
	if [ `echo $?` -ne 0 ]
	then
		echo "Can not ping server 10.0.0.91."
		exit -36
	fi		 
	
	cd /tmp
	retryNumber=0
	waitTime=0
	while [ ${retryNumber} -lt 4 ]
	do 
		retryNumber=`expr ${retryNumber} + 1`
		waitTime=$((2**${retryNumber}))
		ftp -du ftp://test:test@10.0.0.91/%2F"UnitID Folder"/sfs/FQC3/ "${outputFileName}"
		# make sure ftp succeeded.
		if [ `echo $?` -ne 0 ]
		then
			echo "ftp command tries:<${retryNumber}>."
			sleep "${waitTime}"
		else
			break
		fi	
	done
	# Did we finally successfully upload file to ftp?
	if [ ${retryNumber} -eq 4 ]
	then
		echo "After 4x tries, ftp command still failed."
		exit -37
	fi
	# Delete result file
	rm -f "/tmp/${outputFileName}" 		 
}

lcd2_SNmatching()
{
    # LCD2 equals FQC4
	# Need to run mount_afp command to mount afp volumes first
	#if [ ! -d /Users/Shared/ResultTxt/sfs/ ]; then
	#	mount_afp afp://test:test@10.0.0.91/UnitID\ Folder/ /Users/Shared/ResultTxt
	#	sleep 5
	#fi

	#if [ ! -d "/Users/Shared/ResultTxt/sfs/FQC4" ]; then
	#	echo "/Users/Shared/ResultTxt/sfs/FQC4 is not found"
	#	exit -31
	#fi

	if [ ! -f "/Phoenix/Logs/SerialNumber.txt" ]; then
		echo "/Phoenix/Logs/SerialNumber.txt is not found"
		exit -32
	else
		cleanRoom_SI_Report=`cat /Phoenix/Logs/SerialNumber.txt`
		outputFileName=`cat /Phoenix/Logs/SerialNumber.txt`
		outputFileName="${outputFileName}""FQC4.txt"
	fi
	
	if [ "${resultFlag}" == "pass" ]; then
		cleanRoom_SI_Report="${cleanRoom_SI_Report}"",""FQC4"",""${timeStamp}"",""P"","
	else	
		cleanRoom_SI_Report="${cleanRoom_SI_Report}"",""FQC4"",""${timeStamp}"",""F"","
	fi 
	
	# Verify process.plog file existence and read back programmed display SN
    if [ ! -f /Volumes/MaxDisk/Phoenix/Logs/processlog.plog ]; then
        echo "Did not see file /Volumes/MaxDisk/Phoenix/Logs/processlog.plog"
        exit -33
    fi
    # programmedDisplaySN=`cat /Volumes/MaxDisk/Phoenix/Logs/processlog.plog | grep -i 'class="display"' | cut -d , -f 28 | cut -d = -f 2 | cut -d \" -f 2`
    # See script v1.3 release note
    panelDetectOutput=`/TE_Support/Tools/LCD1/PanelDetect.app/Contents/MacOS/PanelDetect -c`
    programmedDisplaySN=`echo "${panelDetectOutput}" | grep -i 'Serial' | cut -d : -f 2 | sed 's/[[^ ]]*//g'`
    
    if [ `echo $?` -ne 0 ]; then
        echo "Errow with parsing programmed SN from processlog.plog."
        exit -34
    fi

	cleanRoom_SI_Report="${cleanRoom_SI_Report}""${programmedDisplaySN}"
	
	# 1.8 Do not capture camera sn any more
	# if [ ! -f "/Indy/Logs/CameraSN.txt" ]; then
		# echo "/Indy/Logs/CameraSN.txt is not found"
		# exit -33
	# else	
		# cameraSN=`cat /Indy/Logs/CameraSN.txt | cut -d ":" -f 2 | awk '{print $1}'`
	# fi
	
	# cleanRoom_SI_Report="${cleanRoom_SI_Report}""${cameraSN}"
		
	echo "${cleanRoom_SI_Report}" > "/tmp/${outputFileName}"
	
	if [ `echo $?` -ne 0 ]; then
		echo "Failed to output the result file"
		exit -35
	fi
	
	# Now it's ready to ftp the file into TIA server with retry logic in place.
	# Ping check TIA server first.
	ping -c 2 10.0.0.91 >/dev/null 2>&1
	if [ `echo $?` -ne 0 ]
	then
		echo "Can not ping server 10.0.0.91."
		exit -36
	fi		 
	
	cd /tmp
	retryNumber=0
	waitTime=0
	while [ ${retryNumber} -lt 4 ]
	do 
		retryNumber=`expr ${retryNumber} + 1`
		waitTime=$((2**${retryNumber}))
		ftp -du ftp://test:test@10.0.0.91/%2F"UnitID Folder"/sfs/FQC4/ "${outputFileName}"
		# make sure ftp succeeded.
		if [ `echo $?` -ne 0 ]
		then
			echo "ftp command tries:<${retryNumber}>."
			sleep "${waitTime}"
		else
			break
		fi	
	done
	# Did we finally successfully upload file to ftp?
	if [ ${retryNumber} -eq 4 ]
	then
		echo "After 4x tries, ftp command still failed."
		exit -37
	fi		 	
	rm -f "/tmp/${outputFileName}" 		 
}

roe_SNmatching()
{
    # ROE needs to remove camera function test and no pass/fail criteria any more. Do not echo "P" or "F" into txt.
	# Need to run mount_afp command to mount afp volumes first
	if [ ! -d /Users/Shared/ResultTxt/sfs/ ]; then
		mount_afp afp://test:test@10.0.0.91/UnitID\ Folder/ /Users/Shared/ResultTxt
		sleep 5
	fi

	if [ ! -d "/Users/Shared/ResultTxt/sfs/ROE" ]; then
		echo "/Users/Shared/ResultTxt/sfs/ROE is not found"
		exit -41
	fi

	if [ ! -f "/Phoenix/Logs/SerialNumber.txt" ]; then
		echo "/Phoenix/Logs/SerialNumber.txt is not found"
		exit -42
	else
		cleanRoom_SI_Report=`cat /Phoenix/Logs/SerialNumber.txt`
		outputFileName=`cat /Phoenix/Logs/SerialNumber.txt`
		outputFileName="${outputFileName}""ROE.txt"
	fi
	
	if [ "${resultFlag}" == "pass" ]; then
		cleanRoom_SI_Report="${cleanRoom_SI_Report}"",""ROE"",""${timeStamp}"",""P"","
	else	
		cleanRoom_SI_Report="${cleanRoom_SI_Report}"",""ROE"",""${timeStamp}"",""P"","
	fi 
	
	if [ ! -f "/Phoenix/Logs/processlog.plog" ]; then
		echo "/Phoenix/Logs/processlog.plog is not found"
		exit -13
	else	
		cameraSN=`cat /Phoenix/Logs/processlog.plog | grep -m 1 'type="Camera"' | sed 's/.*type="Camera".*serialNumber="\(.*\)" & firmwareVersion.*$/\1/'`
	fi
	
	cleanRoom_SI_Report="${cleanRoom_SI_Report}""${cameraSN}"
		
	echo "${cleanRoom_SI_Report}" > "/Users/Shared/ResultTxt/sfs/ROE/${outputFileName}"
	
	if [ `echo $?` -ne 0 ]; then
		echo "Failed to output the result file"
		exit -44
	fi
}

lcd3_SNmatching()
{
    # LCD3 is scanning display panel SN and check agaist programmed SN.
    # Ignore pass/fail argument.
    # Do not generate txt file for checking with SFIS.

    # Verify that SerialNumber.txt file existence and read back scanned SN
    if [ ! -f /Volumes/MaxDisk/Phoenix/Logs/SerialNumber.txt ]; then
        echo "Did not see file /Volumes/MaxDisk/Phoenix/Logs/SerialNumber.txt"
        exit -51
    fi

    # Verify that SerialNumber.txt file existence and read back scanned SN
    scannedSN=`cat /Volumes/MaxDisk/Phoenix/Logs/SerialNumber.txt`

    # Verify process.plog file existence and read back programmed SN
	if [ ! -f /Volumes/MaxDisk/Phoenix/Logs/processlog.plog ]; then
        echo "Did not see file /Volumes/MaxDisk/Phoenix/Logs/processlog.plog"
        exit -52
    fi
    # programmedSN=`cat /Volumes/MaxDisk/Phoenix/Logs/processlog.plog | grep -i 'class="display"' | cut -d , -f 28 | cut -d = -f 2 | cut -d \" -f 2`
    panelDetectOutput=`/TE_Support/Tools/LCD1/PanelDetect.app/Contents/MacOS/PanelDetect -c`
    programmedSN=`echo "${panelDetectOutput}" | grep -i 'Serial' | cut -d : -f 2 | sed 's/[[^ ]]*//g'`
    if [ `echo $?` -ne 0 ]; then
        echo "Errow with parsing programmed SN from processlog.plog."
        exit -53
    fi

    # Do comparing
    if [ "${scannedSN}" != "${programmedSN}" ]; then
        echo "Found unmatched SN. "
        echo "Scanned SN is: ${scannedSN}."
        echo "Programmed display SN is: ${programmedSN}."
        exit -54
    else
        exit 0
    fi
}


cellt_SNmatching()
{
    # LCD2 equals FQC4
	# Need to run mount_afp command to mount afp volumes first
	#if [ ! -d /Users/Shared/ResultTxt/sfs/ ]; then
	#	mount_afp afp://test:test@10.0.0.91/UnitID\ Folder/ /Users/Shared/ResultTxt
	#	sleep 5
	#fi

	#if [ ! -d "/Users/Shared/ResultTxt/sfs/FQC4" ]; then
	#	echo "/Users/Shared/ResultTxt/sfs/FQC4 is not found"
	#	exit -31
	#fi

	if [ ! -f "/Phoenix/Logs/SerialNumber.txt" ]; then
		echo "/Phoenix/Logs/SerialNumber.txt is not found"
		exit -32
	else
		cleanRoom_SI_Report=`cat /Phoenix/Logs/SerialNumber.txt`
		outputFileName=`cat /Phoenix/Logs/SerialNumber.txt`
		outputFileName="${outputFileName}""CellT.txt"
	fi
	
	if [ "${resultFlag}" == "pass" ]; then
		cleanRoom_SI_Report="${cleanRoom_SI_Report}"",""CellT"",""${timeStamp}"",""P"","
	else	
		cleanRoom_SI_Report="${cleanRoom_SI_Report}"",""CellT"",""${timeStamp}"",""F"","
	fi 
	
	# Verify process.plog file existence and read back programmed display SN
    if [ ! -f /Volumes/MaxDisk/Phoenix/Logs/processlog.plog ]; then
        echo "Did not see file /Volumes/MaxDisk/Phoenix/Logs/processlog.plog"
        exit -33
    fi
    # programmedDisplaySN=`cat /Volumes/MaxDisk/Phoenix/Logs/processlog.plog | grep -i 'class="display"' | cut -d , -f 28 | cut -d = -f 2 | cut -d \" -f 2`
    # See script v1.3 release note
    panelDetectOutput=`/TE_Support/Tools/LCD1/PanelDetect.app/Contents/MacOS/PanelDetect -c`
    programmedDisplaySN=`echo "${panelDetectOutput}" | grep -i 'Serial' | cut -d : -f 2 | sed 's/[[^ ]]*//g'`
    
    if [ `echo $?` -ne 0 ]; then
        echo "Errow with parsing programmed SN from processlog.plog."
        exit -34
    fi

	cleanRoom_SI_Report="${cleanRoom_SI_Report}""${programmedDisplaySN}"
	
	# 1.8 Do not capture camera sn any more
	# if [ ! -f "/Indy/Logs/CameraSN.txt" ]; then
		# echo "/Indy/Logs/CameraSN.txt is not found"
		# exit -33
	# else	
		# cameraSN=`cat /Indy/Logs/CameraSN.txt | cut -d ":" -f 2 | awk '{print $1}'`
	# fi
	
	# cleanRoom_SI_Report="${cleanRoom_SI_Report}""${cameraSN}"
		
	echo "${cleanRoom_SI_Report}" > "/tmp/${outputFileName}"
	
	if [ `echo $?` -ne 0 ]; then
		echo "Failed to output the result file"
		exit -35
	fi
	
	# Now it's ready to ftp the file into TIA server with retry logic in place.
	# Ping check TIA server first.
	ping -c 2 10.0.0.91 >/dev/null 2>&1
	if [ `echo $?` -ne 0 ]
	then
		echo "Can not ping server 10.0.0.91."
		exit -36
	fi		 
	
	cd /tmp
	retryNumber=0
	waitTime=0
	while [ ${retryNumber} -lt 4 ]
	do 
		retryNumber=`expr ${retryNumber} + 1`
		waitTime=$((2**${retryNumber}))
		ftp -du ftp://test:test@10.0.0.91/%2F"UnitID Folder"/sfs/CellT/ "${outputFileName}"
		# make sure ftp succeeded.
		if [ `echo $?` -ne 0 ]
		then
			echo "ftp command tries:<${retryNumber}>."
			sleep "${waitTime}"
		else
			break
		fi	
	done
	# Did we finally successfully upload file to ftp?
	if [ ${retryNumber} -eq 4 ]
	then
		echo "After 4x tries, ftp command still failed."
		exit -37
	fi		 	
	rm -f "/tmp/${outputFileName}" 	
}


ll_SNmatching()
{
	if [ ! -f "/Phoenix/Logs/SerialNumber.txt" ]; then
		echo "/Phoenix/Logs/SerialNumber.txt is not found"
		exit -32
	else
		cleanRoom_SI_Report=`cat /Phoenix/Logs/SerialNumber.txt`
		outputFileName=`cat /Phoenix/Logs/SerialNumber.txt`
		outputFileName="${outputFileName}""LLCUC.txt"
	fi
	
	if [ "${resultFlag}" == "pass" ]; then
		cleanRoom_SI_Report="${cleanRoom_SI_Report}"",""LLCU"",""${timeStamp}"",""P"","
	else	
		cleanRoom_SI_Report="${cleanRoom_SI_Report}"",""LLCU"",""${timeStamp}"",""F"","
	fi 
	
	# Verify process.plog file existence and read back programmed display SN
    if [ ! -f /Volumes/MaxDisk/Phoenix/Logs/processlog.plog ]; then
        echo "Did not see file /Volumes/MaxDisk/Phoenix/Logs/processlog.plog"
        exit -33
    fi
    # programmedDisplaySN=`cat /Volumes/MaxDisk/Phoenix/Logs/processlog.plog | grep -i 'class="display"' | cut -d , -f 28 | cut -d = -f 2 | cut -d \" -f 2`
    # See script v1.3 release note
    panelDetectOutput=`/TE_Support/Tools/LCD1/PanelDetect.app/Contents/MacOS/PanelDetect -c`
    programmedDisplaySN=`echo "${panelDetectOutput}" | grep -i 'Serial' | cut -d : -f 2 | sed 's/[[^ ]]*//g'`
    
    if [ `echo $?` -ne 0 ]; then
        echo "Errow with parsing programmed SN from processlog.plog."
        exit -34
    fi
    
    # Get fixture camera SN and do rough check
    fixtureCameraSN=`cat /Phoenix/Logs/processlog.plog | grep -m 1 'CameraSerial=' | cut -d "," -f 5 | cut -d "=" -f 3 | cut -d '"' -f 1`
    echo "Parsed fixture camera SN is: ${fixtureCameraSN}."
    #if [ ! `echo "${fixtureCameraSN}" | wc -c | sed  's/[[^ ]]*//g'` -gt 1 ]; then
    #    echo "Length verification for Parsed fixture camera SN failed."
    #    exit -64
    #fi

	cleanRoom_SI_Report="${cleanRoom_SI_Report}""${programmedDisplaySN}"",""${fixtureCameraSN}"
	
	# 1.8 Do not capture camera sn any more
	# if [ ! -f "/Indy/Logs/CameraSN.txt" ]; then
		# echo "/Indy/Logs/CameraSN.txt is not found"
		# exit -33
	# else	
		# cameraSN=`cat /Indy/Logs/CameraSN.txt | cut -d ":" -f 2 | awk '{print $1}'`
	# fi
	
	# cleanRoom_SI_Report="${cleanRoom_SI_Report}""${cameraSN}"
		
	echo "${cleanRoom_SI_Report}" > "/tmp/${outputFileName}"
	
	if [ `echo $?` -ne 0 ]; then
		echo "Failed to output the result file"
		exit -35
	fi
	
	# Now it's ready to ftp the file into TIA server with retry logic in place.
	# Ping check TIA server first.
	ping -c 2 10.0.0.91 >/dev/null 2>&1
	if [ `echo $?` -ne 0 ]
	then
		echo "Can not ping server 10.0.0.91."
		exit -36
	fi		 
	
	cd /tmp
	retryNumber=0
	waitTime=0
	while [ ${retryNumber} -lt 4 ]
	do 
		retryNumber=`expr ${retryNumber} + 1`
		waitTime=$((2**${retryNumber}))
		ftp -du ftp://test:test@10.0.0.91/%2F"UnitID Folder"/sfs/LLCUC/ "${outputFileName}"
		# make sure ftp succeeded.
		if [ `echo $?` -ne 0 ]
		then
			echo "ftp command tries:<${retryNumber}>."
			sleep "${waitTime}"
		else
			break
		fi	
	done
	# Did we finally successfully upload file to ftp?
	if [ ${retryNumber} -eq 4 ]
	then
		echo "After 4x tries, ftp command still failed."
		exit -37
	fi		 	
	rm -f "/tmp/${outputFileName}" 	
}

cu_SNmatching()
{
	if [ ! -f "/Phoenix/Logs/SerialNumber.txt" ]; then
		echo "/Phoenix/Logs/SerialNumber.txt is not found"
		exit -32
	else
		cleanRoom_SI_Report=`cat /Phoenix/Logs/SerialNumber.txt`
		outputFileName=`cat /Phoenix/Logs/SerialNumber.txt`
		outputFileName="${outputFileName}""CLUT.txt"
	fi
	
	if [ "${resultFlag}" == "pass" ]; then
		cleanRoom_SI_Report="${cleanRoom_SI_Report}"",""CLUT"",""${timeStamp}"",""P"","
	else	
		cleanRoom_SI_Report="${cleanRoom_SI_Report}"",""CLUT"",""${timeStamp}"",""F"","
	fi 
	
	# Verify process.plog file existence and read back programmed display SN
    if [ ! -f /Volumes/MaxDisk/Phoenix/Logs/processlog.plog ]; then
        echo "Did not see file /Volumes/MaxDisk/Phoenix/Logs/processlog.plog"
        exit -33
    fi
    # programmedDisplaySN=`cat /Volumes/MaxDisk/Phoenix/Logs/processlog.plog | grep -i 'class="display"' | cut -d , -f 28 | cut -d = -f 2 | cut -d \" -f 2`
    # See script v1.3 release note
    panelDetectOutput=`/TE_Support/Tools/LCD1/PanelDetect.app/Contents/MacOS/PanelDetect -c`
    programmedDisplaySN=`echo "${panelDetectOutput}" | grep -i 'Serial' | cut -d : -f 2 | sed 's/[[^ ]]*//g'`
    
    if [ `echo $?` -ne 0 ]; then
        echo "Errow with parsing programmed SN from processlog.plog."
        exit -34
    fi

	cleanRoom_SI_Report="${cleanRoom_SI_Report}""${programmedDisplaySN}"
	
	# 1.8 Do not capture camera sn any more
	# if [ ! -f "/Indy/Logs/CameraSN.txt" ]; then
		# echo "/Indy/Logs/CameraSN.txt is not found"
		# exit -33
	# else	
		# cameraSN=`cat /Indy/Logs/CameraSN.txt | cut -d ":" -f 2 | awk '{print $1}'`
	# fi
	
	# cleanRoom_SI_Report="${cleanRoom_SI_Report}""${cameraSN}"
		
	echo "${cleanRoom_SI_Report}" > "/tmp/${outputFileName}"
	
	if [ `echo $?` -ne 0 ]; then
		echo "Failed to output the result file"
		exit -35
	fi
	
	# Now it's ready to ftp the file into TIA server with retry logic in place.
	# Ping check TIA server first.
	ping -c 2 10.0.0.91 >/dev/null 2>&1
	if [ `echo $?` -ne 0 ]
	then
		echo "Can not ping server 10.0.0.91."
		exit -36
	fi		 
	
	cd /tmp
	retryNumber=0
	waitTime=0
	while [ ${retryNumber} -lt 4 ]
	do 
		retryNumber=`expr ${retryNumber} + 1`
		waitTime=$((2**${retryNumber}))
		ftp -du ftp://test:test@10.0.0.91/%2F"UnitID Folder"/sfs/CLUT/ "${outputFileName}"
		# make sure ftp succeeded.
		if [ `echo $?` -ne 0 ]
		then
			echo "ftp command tries:<${retryNumber}>."
			sleep "${waitTime}"
		else
			break
		fi	
	done
	# Did we finally successfully upload file to ftp?
	if [ ${retryNumber} -eq 4 ]
	then
		echo "After 4x tries, ftp command still failed."
		exit -37
	fi		 	
	rm -f "/tmp/${outputFileName}" 	
}



case "${stationFlag}" in
"CBTS")
    echo "Processing CBTS."
    cbts_SNmatching
    ;;
"CBT")
    echo "Processing CBT."
    cbt_SNmatching
    ;;
"CellT")
    echo "Processing CellT."
    cellt_SNmatching
    ;;     
"REIN")
    echo "Processing ROE."
    rein_SNmatching
    ;;
"LCD1")
    echo "Processing LCD1."
    lcd1_SNmatching
    ;;
"LCD2")
    echo "Processing LCD2."
    lcd2_SNmatching
    ;;
"ROE")
    echo "Processing ROE."
    roe_SNmatching
    ;;
"LCD3")
    echo "Processing LCD3."
    lcd3_SNmatching
    ;;
"LL")
    echo "Processing LL."
    ll_SNmatching
    ;;
"CU")
    echo "Processing CU."
    cu_SNmatching
    ;;
*)
	echo "Unexpected incoming argument. Quit with returning error code."
	exit -1
	;;
esac



