#!/bin/sh

echo "Check if Panel is LGD.."

PanelVendor=`/TE_Support/Scripts/Test_Process/TCONConfigUpdater1.10.app/Contents/MacOS/TCONConfigUpdater -c | grep -c "LGD"`


if [ $PanelVendor -eq 1 ]; then
	echo "LGD Panel detected."
	exit 0
else
	echo "LGD Panel not detected."
	exit 1
fi 
