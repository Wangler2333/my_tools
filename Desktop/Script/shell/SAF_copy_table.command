#!/bin/sh

rm -rf /Phoenix/Tables

cp -a /Volumes/DATA/FDR_Seal/ShipAsFail/GeneralPreference.plist /Phoenix/Configuration
cp -a /Volumes/DATA/FDR_Seal/ShipAsFail/Tables /Phoenix/
#cp -a /Volumes/DATA/ShipAsFail/Tables.zip /Phoenix/

cp /Volumes/DATA/FDR_Seal/ShipAsFail/Rule/config_default_phoenix_SS_NoThaw.txt /Phoenix/Tools/Settings/

#cp -R /Volumes/build/FDR_Seal/Factory_PR/* /AppleInternal/FactoryRestoreDocuments/Factory

sleep 3

diskutil unmount /Volumes/LUCY 

/TE_Support/Scripts/Test_Process/cleanup_Phoenix2.command
sleep 1
#/TE_Support/Scripts/Test_Process/start_command_c
cp -rf /Volumes/LUCY/FDR_Seal/Check_M8.command /private/var/root/Desktop
/private/var/root/Desktop/Check_M8.command

reboot

