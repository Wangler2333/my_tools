#!/bin/sh

killall PhoenixCE
killall miniT

sleep 1

cp -rf /Volumes/DATA/J79ByPassFix /private/var/root/Desktop
cp -rf /Volumes/DATA/SigningBypass.psplist /Phoenix/Configuration
cp -rf /Volumes/DATA/GeneralPreference.plist /Phoenix/Configuration

sleep 1

/private/var/root/Desktop/J79ByPassFix

sleep 1

/TE_Support/Scripts/Test_Process/start_command_c