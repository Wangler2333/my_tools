#!/bin/sh

/TE_Support/Scripts/Test_Process/cleanup_Phoenix2.command

cp -rf /private/var/root/Desktop/EE_DOE/CollectDesktopLog.command /Phoenix
cp -rf /private/var/root/Desktop/EE_DOE/genSystemSN.sh /
rm -rf /Phoenix/Tables
cp -rf /private/var/root/Desktop/EE_DOE/shmoo/Tables /Phoenix
rm -rf /Phoenix/Configuration/configExpected.txt 
cp -rf /private/var/root/Desktop/EE_DOE/configExpected.txt /Phoenix/Configuration
＃rm -rf /Phoenix/Configuration/GeneralPreference.plist
＃cp -rf /private/var/root/Desktop/EE_DOE/shmoo/GeneralPreference.plist /Phoenix/Configuration

#TableVar=`find /Phoenix/Tables -name *tbproj | sed 's/.*\///'`

#cat /Phoenix/Tables/$TableVar/product.tbseq | sed -e 's/<sequencelist default_seq="Standard">/<sequencelist default_seq="Shmoo">/g’ /Phoenix/Tables/$TableVar/product.tbseq >> /Phoenix/Logs/product1.tbseq
#mv /Phoenix/Logs/product1.tbseq /Phoenix/Tables/$TableVar/product.tbseq


sleep 1

reboot