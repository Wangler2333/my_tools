#!/bin/sh


# J52 Euphony Retest Process Control by Script to check B102 Dongle SN;
# Check script parameter and confirm how many Euphony test has been done:
# "Normal" is for the first time of normal test;
# "FirstRetryOnTheSameFixture" is for the first retry on the same fixture with pulling out unit from box and sending in again;
# "SecondRetryOnDifferentFixture" is for the second retry on different fixture;
# "ThirdRetryAfterThreeHours" is for the third retry on different fixture than 1st and 2nd;
# "ForthRetry" is for the forth retry on different fixture than 1st, 2nd and 3rd.


# Define a function to capture 
CaptureDongle()
{
	echo "Call function to make sure the dongle was captured"
	# Use loops to check the dongle
	while [ `ioreg -b -w 0 -l | grep -c '"USB Product Name" = "Apple USB Ethernet Adapter"'` -ne 1 ]
	do 
		echo "System Did not detect dongle and will keep detecting every 10 seconds"
		sleep 10
	done	
	echo "System detect the dongle successfully"	
}

# Define a function to capture 
GetDongleSN()
{
	echo "Call function to get the dongle serial number"
	if [ "$1" == "One" ]
	then 
		USBSN_One=`ioreg -b -w 0 -l | grep -A 18 '"USB Product Name" = "Apple USB Ethernet Adapter"' | grep '"USB Serial Number"' | awk -F \" '{print $4}'`
		echo "J52_FATP_Euphony_USBSN_One:${USBSN_One}" >> /Phoenix/Logs/Euphony_Dongle_SN.log
	elif [ "$1" == "Two" ]
	then 
		USBSN_Two=`ioreg -b -w 0 -l | grep -A 18 '"USB Product Name" = "Apple USB Ethernet Adapter"' | grep '"USB Serial Number"' | awk -F \" '{print $4}'`
		echo "J52_FATP_Euphony_USBSN_Two:${USBSN_Two}" >> /Phoenix/Logs/Euphony_Dongle_SN.log
	elif [ "$1" == "Three" ]
	then 
		USBSN_Three=`ioreg -b -w 0 -l | grep -A 18 '"USB Product Name" = "Apple USB Ethernet Adapter"' | grep '"USB Serial Number"' | awk -F \" '{print $4}'`
		echo "J52_FATP_Euphony_USBSN_Three:${USBSN_Three}" >> /Phoenix/Logs/Euphony_Dongle_SN.log
	elif [ "$1" == "Four" ]
	then 
		USBSN_Four=`ioreg -b -w 0 -l | grep -A 18 '"USB Product Name" = "Apple USB Ethernet Adapter"' | grep '"USB Serial Number"' | awk -F \" '{print $4}'`
		echo "J52_FATP_Euphony_USBSN_Four:${USBSN_Four}" >> /Phoenix/Logs/Euphony_Dongle_SN.log
	elif [ "$1" == "Five" ]
	then 
		USBSN_Five=`ioreg -b -w 0 -l | grep -A 18 '"USB Product Name" = "Apple USB Ethernet Adapter"' | grep '"USB Serial Number"' | awk -F \" '{print $4}'`
		echo "J52_FATP_Euphony_USBSN_Five:${USBSN_Five}" >> /Phoenix/Logs/Euphony_Dongle_SN.log
	else
		echo "Please check the parameter"
	fi		
}


# Main process starts from here
if [ $# == 1 ] && [ "$1" == "Normal" ]
then 
	# Normal test and make sure no SC test record in Phoenix test logs
	# Make sure dongle was captured right before performing SC test. 
	echo "Normal Euphony test" 
	
	CaptureDongle
	
	GetDongleSN "One"
	
elif [ $# == 1 ] && [ "$1" == "FirstRetryOnTheSameFixture" ]
then
	# First Retry: Make sure the dongle serial number is not changed and previous phoenix process logs only have 1 record of Euphony test 
	# Make sure dongle was captured right before performing Euphony test. 
	# Further improvement: If unit has been held for very long time, handle it.
	echo "First Retry: Make sure the dongle serial number is not changed"
	# Get the USB dongle SN captured during the normal Euphony test
	USBDongleSNOne=`cat /Phoenix/Logs/Euphony_Dongle_SN.log | grep 'J52_FATP_Euphony_USBSN_One' | cut -d , -f 5 | cut -d : -f 2 | cut -d \" -f 1`
	# Check how many times of Euphony test has been performed by tracking the phoenix logs. Note that this should take a few seconds
	# This can be a further improvement
	
	CaptureDongle
	# Get the dongle SN of First Retry

	# If the dongle SN is different with the previous one, looping and detecting until dongle match
	while [ 1 ]
	do
		CaptureDongle
		CurrentDongle=`ioreg -b -w 0 -l | grep -A 18 '"USB Product Name" = "Apple USB Ethernet Adapter"' | grep '"USB Serial Number"' | awk -F \" '{print $4}'`
		if [ "${CurrentDongle}" != "${USBDongleSNOne}" ]
		then
		    open /TE_Support/Images/SameFixture.png
			echo "The USB dongle SN detected during first retry does not match with the one detected during normal Euphony test"
			echo "Delay 15 seconds and then capture the dongle SN again"
			sleep 15			
		else
			echo "The USB dongle SN detected during first retry match with the one detected during normal Euphony test, good to do Euphony test"
			GetDongleSN "Two"
			killall Preview
			break
		fi
	done
			
elif [ $# == 1 ] && [ "$1" == "SecondRetryOnDifferentFixture" ]
then
	# Second Retry: Make sure the dongle serial number is different and previous phoenix process logs have 2 records of Euphony test
	# Make sure dongle was captured right before performing Euphony test. 
	echo "Second Retry: Make sure the dongle serial number is different"
	# Get the USB dongle SN captured during the normal Euphony test
	USBDongleSNOne=`cat /Phoenix/Logs/Euphony_Dongle_SN.log | grep 'J52_FATP_Euphony_USBSN_One' | cut -d , -f 5 | cut -d : -f 2 | cut -d \" -f 1`

	CaptureDongle
	
	# If the dongle SN is different with the previous one, looping and detecting until dongle match
	while [ 1 ]
	do
		CaptureDongle
		CurrentDongle=`ioreg -b -w 0 -l | grep -A 18 '"USB Product Name" = "Apple USB Ethernet Adapter"' | grep '"USB Serial Number"' | awk -F \" '{print $4}'`
		if [ "${CurrentDongle}" == "${USBDongleSNOne}" ]
		then
		    open /TE_Support/Images/DiffFixture.png
			echo "The USB dongle SN detected during second retry match with the one detected during normal Euphony test"
			echo "Delay 15 seconds and then capture the dongle SN again"
			sleep 15			
		else
			echo "The USB dongle SN detected during first retry is different from the one detected during normal Euphony test, good to do Euphony test"
			GetDongleSN "Three"
			killall Preview
			break
		fi
	done
	
elif [ $# == 1 ] && [ "$1" == "ThirdRetryOnDifferentFixture" ]
then
	# Third Retry: Make sure the dongle serial number is different and previous phoenix process logs have 3 records of Euphony test
	# Make sure dongle was captured right before performing Euphony test. 
	echo "Third Retry: Make sure the dongle serial number is different"
	# Get the USB dongle SN captured during the normal Euphony test
	USBDongleSNOne=`cat /Phoenix/Logs/Euphony_Dongle_SN.log | grep 'J52_FATP_Euphony_USBSN_One' | cut -d , -f 5 | cut -d : -f 2 | cut -d \" -f 1`
	USBDongleSNThree=`cat /Phoenix/Logs/Euphony_Dongle_SN.log | grep 'J52_FATP_Euphony_USBSN_Three' | cut -d , -f 5 | cut -d : -f 2 | cut -d \" -f 1`

	CaptureDongle
	
	# If the dongle SN is different with the previous one, looping and detecting until dongle match
	while [ 1 ]
	do
		CaptureDongle
		CurrentDongle=`ioreg -b -w 0 -l | grep -A 18 '"USB Product Name" = "Apple USB Ethernet Adapter"' | grep '"USB Serial Number"' | awk -F \" '{print $4}'`
		if [ "${CurrentDongle}" == "${USBDongleSNOne}" ] || [ "${CurrentDongle}" == "${USBDongleSNThree}" ];
		then
		    open /TE_Support/Images/DiffFixture.png
			echo "The USB dongle SN detected during third retry match with the one detected during previous Euphony test"
			echo "Delay 15 seconds and then capture the dongle SN again"
			sleep 15			
		else
			echo "The USB dongle SN detected during Third retry is different from the one detected during previous Euphony test, good to do Euphony test"
			GetDongleSN "Four"
			killall Preview
			break
		fi
	done
	
elif [ $# == 1 ] && [ "$1" == "ForthRetryOnDifferentFixture" ]
then
	# Forth Retry: Make sure the dongle serial number is different and previous phoenix process logs have 4 records of Euphony test
	# Make sure dongle was captured right before performing Euphony test. 
	echo "Forth Retry: Make sure the dongle serial number is different"
	# Get the USB dongle SN captured during the previous Euphony test
	USBDongleSNOne=`cat /Phoenix/Logs/Euphony_Dongle_SN.log | grep 'J52_FATP_Euphony_USBSN_One' | cut -d , -f 5 | cut -d : -f 2 | cut -d \" -f 1`
	USBDongleSNThree=`cat /Phoenix/Logs/Euphony_Dongle_SN.log | grep 'J52_FATP_Euphony_USBSN_Three' | cut -d , -f 5 | cut -d : -f 2 | cut -d \" -f 1`
	USBDongleSNFour=`cat /Phoenix/Logs/Euphony_Dongle_SN.log | grep 'J52_FATP_Euphony_USBSN_Four' | cut -d , -f 5 | cut -d : -f 2 | cut -d \" -f 1`

	CaptureDongle
		
	# If the dongle SN is different with the previous one, looping and detecting until dongle match
	while [ 1 ]
	do
		CaptureDongle
		CurrentDongle=`ioreg -b -w 0 -l | grep -A 18 '"USB Product Name" = "Apple USB Ethernet Adapter"' | grep '"USB Serial Number"' | awk -F \" '{print $4}'`
		if ([ "${CurrentDongle}" == "${USBDongleSNOne}" ]) || ([ "${CurrentDongle}" == "${USBDongleSNThree}" ]) || ([ "${CurrentDongle}" == "${USBDongleSNFour}" ])
		then
		    open /TE_Support/Images/DiffFixture.png
			echo "The USB dongle SN detected during fourth retry match with the one detected during previous Euphony test"
			echo "Delay 15 seconds and then capture the dongle SN again"
			sleep 15			
		else
			echo "The USB dongle SN detected during fourth retry is different from the one detected during previous Euphony test, good to do Euphony test"
			GetDongleSN "Five"
			killall Preview
			break
		fi
	done
		
else
	echo "Either the number of script parameter is not equal 1 or the parameter is not expected"
fi	



