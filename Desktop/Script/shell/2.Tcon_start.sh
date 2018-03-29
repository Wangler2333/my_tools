#!/bin/sh

/TE_Support/Scripts/Test_Process/cleanup_Phoenix2.command

cp -rf /private/var/root/Desktop/EE_DOE/CollectDesktopLog.command /Phoenix
cp -rf /private/var/root/Desktop/EE_DOE/genSystemSN.sh /
rm -rf /Phoenix/Tables
cp -rf /private/var/root/Desktop/EE_DOE/TCON/Tables /Phoenix
cp -rf /private/var/root/Desktop/EE_DOE/running /Phoenix/Product
rm -rf /Phoenix/Configuration/configExpected.txt 
cp -rf /private/var/root/Desktop/EE_DOE/configExpected.txt /Phoenix/Configuration
rm -rf /TE_Support/Tools/Phoenix/PhoenixCE.app
cp -rf /private/var/root/Desktop/EE_DOE/PhoenixCE.app /TE_Support/Tools/Phoenix
rm -rf /Phoenix/Configuration/GeneralPreference.plist
cp -rf /private/var/root/Desktop/EE_DOE/TCON/GeneralPreference.plist /Phoenix/Configuration
rm -rf /TE_Support/Scripts/Test_Process/startup_phoenix.command
cp -rf /private/var/root/Desktop/EE_DOE/startup_phoenix.command /TE_Support/Scripts/Test_Process



sleep 1

reboot