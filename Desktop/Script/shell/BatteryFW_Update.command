#!/bin/sh

SystemSN=`system_profiler SPHardwareDataType | grep "Serial" | sed 's/.*: //'`
LogSN=`cat < SerialNumber.txt`

CheckAdaptor()
{
   isConnected=`system_profiler SPPowerDataType | grep "Connected:" | sed 's/.*: //'`
   while [ "$isConnected" != "Yes" ]
   do
   echo "AC not connected"
   sleep 1
   isConnected=`system_profiler SPPowerDataType | grep "Connected:" | sed 's/.*: //'`
   done   
}
USB_Match()
{
   UUID=`diskutil info /Volumes/DATA | grep "Volume UUID:" | sed 's/.*: //'`
   IFS=' '
   UUID_DATA="AF652AAA-0363-3D17-A046-D1FCC5A47565"
   if [ $UUID == $UUID_DATA ];then 
     echo "[PASS]MATCHED"
   else
     echo "[FAIL]MISMATCH" ; exit 1
   fi
}

CheckAdaptor

USB_Match

expect -c "spawn hdiutil attach /Volumes/DATA/BatteryFW_Update.dmg; expect -re \".*password*\"; send \"J79Update\r\"; expect -re \"$\"; send \"exit 0\r\"; interact"
#expect -c "spawn hdiutil attach -readonly $SCRIPT_DIR/BatteryFW_Update.dmg; expect -re \".*password*\"; send \"J79Update\r\"; expect -re \"$\"; send \"exit 0\r\"; interact"

Times=`cat < /Volumes/BatteryFW_Update/Times.txt | grep -c 1`

if [ $Times -eq 30 ];then
   rm -rf /Volumes/DATA/BatteryFW_Update.dmg
   rm -rf /System/Library/LaunchAgents/com.apple.startphoenix.plist
   hdiutil detach /Volumes/BatteryFW_Update ; exit 1
fi

   echo 1 >> /Volumes/BatteryFW_Update/Times.txt
   echo "------------------------" >> /Volumes/BatteryFW_Update/SN.txt
   echo $SystemSN >> /Volumes/BatteryFW_Update/SN.txt
   echo $LogSN >> /Volumes/BatteryFW_Update/SN.txt
   echo "------------------------" >> /Volumes/BatteryFW_Update/SN.txt

cp -rf /Volumes/BatteryFW_Update/Python.framework.zip /Library/Frameworks
rm -rf /Library/Frameworks/Python.framework
cd /Library/Frameworks
unzip Python.framework.zip ; sleep 1
rm -rf /Library/Frameworks/Python.framework.zip
cp -rf /Volumes/BatteryFW_Update/Battery /AppleInternal/Diagnostics/Logs
cp -rf /Volumes/BatteryFW_Update/bmu_updater /Users/Shared
cp -rf /Volumes/BatteryFW_Update/BMU / 

hdiutil detach /Volumes/BatteryFW_Update 

/BMU/J79_upgrade.command

rm -rf /BMU
rm -rf /AppleInternal/Diagnostics/Logs/Battery
rm -rf /Users/Shared/bmu_updater
rm -rf /Library/Frameworks/Python.framework
rm -rf /System/Library/LaunchAgents/com.apple.startphoenix.plist

sleep 2
reboot  