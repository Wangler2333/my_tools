#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time     : 2018/3/17下午3:19
# @Author   : Saseny Zhou
# @Site     : 
# @File     : versionRead.py
# @Software : PyCharm


SystemVersionReadCommand = """
#!/bin/sh
path=/AppleInternal/Diagnostics/OS/Plugins
Result_plugin=/private/var/root/Desktop/plugin_Version.txt

fpath=/Library/Frameworks
Result_framework=/private/var/root/Desktop/framework_Version.txt

Result_kext=/private/var/root/Desktop/kext_Version.txt

dti=$1

#if [ -f $Result_plugin ];then
#Result_plugin=/private/var/root/Desktop/plugin_new.txt
#else 
#Result_plugin=/private/var/root/Desktop/plugin.txt
#fi


OS_Version=`system_profiler SPSoftwareDataType | grep "System Version:" | awk -F ': ' '{print $NF}'`
BootRom_Version=`system_profiler SPHardwareDataType | grep "Boot ROM Version:" | awk -F ': ' '{print $NF}'`
Smc_Version=`system_profiler SPHardwareDataType | grep "SMC Version" | awk -F ': ' '{print $NF}'`
Model=`system_profiler SPHardwareDataType | grep "Model Identifier" | awk -F ': ' '{print $NF}'`
Bluetooth_Version=`system_profiler SPBluetoothDataType | grep "Firmware Version:" | head -1 | awk -F ': ' '{print $NF}'`
Thunderbolt_Version=`system_profiler SPThunderboltDataType | grep "Firmware Version:" | head -1 | awk -F ': ' '{print $NF}'`
Trackpad_ST_Version=`system_profiler SPSPIDataType | grep "Version" | awk -F ': ' '{print $NF}'`
macID=`ioreg -l|grep "board-id" |awk '{print substr($4,3,length($4)-4)}'`
AirPort_Version=`system_profiler SPAirPortDataType | grep "Firmware Version:" | awk -F ': ' '{print$NF}'`

echo "DTI Information:" > $dti
echo "OS Version:	$OS_Version" >> $dti
echo "Model:	$Model" >> $dti
echo "Mac-id:	$macID" >> $dti
echo "EFI BR:	$BootRom_Version" >> $dti
echo "SMC:	$Smc_Version" >> $dti
echo "BluetoohFW:	$Bluetooth_Version" >> $dti
echo "ThunderboltFW:	$Thunderbolt_Version" >> $dti
echo "STFW:	$Trackpad_ST_Version" >> $dti
echo "BroadCom FW:	$AirPort_Version" >> $dti

echo "\n\n\n"  >> $dti
echo "************Plugin********************"   >> $dti
for plugin in `find $path -type d -name *plugin`; do
PluginName=`echo $plugin | sed 's/.*\///'`
cd "$plugin/Contents/"
PluginVersion=`cat "$plugin/Contents/Info.plist" | grep -A 1 "CFBundleShortVersionString" | grep string | sed 's/string\>//g' | sed 's/\<//g' | sed 's/\///'`
#echo "$PluginName	$PluginVersion" >> $Result_plugin
echo "$PluginName	$PluginVersion" >> $dti
done

echo "\n\n\n"  >> $dti
echo "************Framework********************"   >> $dti
for framework in `find $fpath -type d -name *.framework`; do
FrameworkName=`echo $framework | sed 's/.*\///'`
FrameworkVersion=`cat $framework/Versions/A/Resources/Info.plist | grep -A 1 "CFBundleShortVersionString" | grep string | sed 's/string\>//g' | sed 's/\<//g' | sed 's/\///'`
#echo "$FrameworkName	$FrameworkVersion" >> $Result_framework
echo "$FrameworkName	$FrameworkVersion" >> $dti
done

echo "\n\n\n"  >> $dti
echo "************Kext********************"   >> $dti
#kextstat | sed 's/.*com/com/' | sed 's/<.*//' > $Result_kext
kextstat | sed 's/.*com/com/' | sed 's/<.*//' >> $dti

"""