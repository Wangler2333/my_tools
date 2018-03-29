#!/bin/sh

echo "Check if Panel is SEC.."

PanelVendor=`/TE_Support/Scripts/Test_Process/TCONConfigUpdater1.10.app/Contents/MacOS/TCONConfigUpdater -c | grep -c "SEC"`


if [ $PanelVendor -eq 1 ]; then
	echo "SEC Panel detected."
	exit 0
else
	echo "SEC Panel not detected."
	exit 1
fi 
