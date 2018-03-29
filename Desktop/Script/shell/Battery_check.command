#!/bin/sh

Battery_Status=`system_profiler SPPowerDataType | grep "Battery Installed" | sed 's/\ //g'`
echo "$Battery_Status"

case $Battery_Status in
*"BatteryInstalled:Yes"* )
echo "System is FrankenPack"
cp -rf /Phoenix/Product/J79_FrankenPack/Tables /Phoenix
cp -rf /Phoenix/Product/J79_FrankenPack/GeneralPreference.plist /Phoenix/Configuration
cp -rf /Phoenix/Product/J79_FrankenPack/Tables.zip /Phoenix

touch /Phoenix/Product/running
;;

*"BatteryInstalled:No"* )
echo "System is Mechanical"
cp -rf /Phoenix/Product/J79_Mechanical/Tables /Phoenix
cp -rf /Phoenix/Product/J79_Mechanical/GeneralPreference.plist /Phoenix/Configuration
cp -rf /Phoenix/Product/J79_Mechanical/Tables.zip /Phoenix

touch /Phoenix/Product/running
;;

esac


