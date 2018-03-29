#!/bin/sh

#cp /Volumes/SDHCMEDIA/J137_FATP_Runin_PTF.json /AppleInternal/Diagnostics/Resources/93
#mv /Library/LaunchAgents/com.apple.hwte.testd.plist /Library/LaunchDaemons
#sleep 1

echo "Set Nvram"

#cp /Tools/boot.efi /Volumes/DIAG/


nvram boot-args="debug=0x8c4e -v kdp_match_name=serial sdxc=0xA0000 dither=0 watchdog=0 blc_disable_fault=1 medetect_panic=1 tb=0x400 usb-no-rtpc=1 intcoproc_unrestricted=1 serial=3"
sleep 1
nvram bcm-ethernet-options='LowPowerEnergyDetect=false'
sleep 1
nvram IONVRAM-SYNCNOW-PROPERTY="IONVRAM-SYNCNOW-PROPERTY"
sleep 5
nvram caterr-reset-disable=%01
reboot


