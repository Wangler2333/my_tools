#!/bin/sh

#Pre-check whether WiFi#2912(Throttle assertion test) could work or not by modify MSWA
#If cannot work,will re-flash BT FW again

#Read initial MSWA status,should be 0
MSWA_0=`/usr/local/bin/wl ccgpioin`
echo "MSWA_0=$MSWA_0"

if [ "$MSWA_0" == "4255 (0x109f)" ]; then
	echo "initial MSWA is 0"
	
	#Set MSWA to 1
	/AppleInternal/Diagnostics/Tools/ypc2 -wdk MSWA 1
	MSWA_1=`/usr/local/bin/wl ccgpioin`
	echo "MSWA_1=$MSWA_1"
	
	if [ "$MSWA_1" == "4251 (0x109b)" ]; then
		echo "Set MSWA to 1 successfully !!!"
		
		#Set MSWA back to initial status 0
		/AppleInternal/Diagnostics/Tools/ypc2 -wdk MSWA 0
		MSWA_2=`/usr/local/bin/wl ccgpioin`
		echo "MSWA_2=$MSWA_2"
		
		if [ "$MSWA_2" == "4255 (0x109f)" ]; then
			echo "PASS,initial MSWA back to 0 !!!"
			exit 0
		else
			echo "FAIL,BT SW corrupted,need re-flash !!!"
			/Firmware/J52BackRevBluetoothFirmwareV79/20703A1_X87_Firmware_Updater_v79.app/Contents/Resources/DFUTool /Firmware/J52BackRevBluetoothFirmwareV79/20703A1_X87_Firmware_Updater_v79.app/Contents/Resources/X87_BCM20703A1_001.001.079.0155.0243.dfu
			/AppleInternal/Diagnostics/Tools/ypc2 -wdk MSWA 0
			exit 1
		fi
	else 
		echo "FAIL,cannot set MSWA to 1,BT SW corrupted,need re-flash !!!"
		/Firmware/J52BackRevBluetoothFirmwareV79/20703A1_X87_Firmware_Updater_v79.app/Contents/Resources/DFUTool /Firmware/J52BackRevBluetoothFirmwareV79/20703A1_X87_Firmware_Updater_v79.app/Contents/Resources/X87_BCM20703A1_001.001.079.0155.0243.dfu
		/AppleInternal/Diagnostics/Tools/ypc2 -wdk MSWA 0
		exit 1
	fi
else
	echo "FAIL,MSWA_0 wrong,BT SW corrupted,need re-flash !!!"
	/Firmware/J52BackRevBluetoothFirmwareV79/20703A1_X87_Firmware_Updater_v79.app/Contents/Resources/DFUTool /Firmware/J52BackRevBluetoothFirmwareV79/20703A1_X87_Firmware_Updater_v79.app/Contents/Resources/X87_BCM20703A1_001.001.079.0155.0243.dfu
	/AppleInternal/Diagnostics/Tools/ypc2 -wdk MSWA 0
	exit 1
fi