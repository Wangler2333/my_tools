#!/bin/sh

Router=`networksetup -getinfo "Apple USB Ethernet Adapter" | grep "Router:" | head -1 | awk -F ': ' '{print $NF}'`
echo "Router IP: $Router"
ping -t 3 $Router | grep -c "3 packets received"
PIavail=$?

if [ $PIavail -ne 0 ]; then
	ping -t 3 $Router | grep -c "3 packets received"
	secondPI=$?
	if [ $secondPI -ne 0 ]; then
		echo "Ping not successfully!"
		exit 1
	fi
fi

echo "Successfully Ping $Router - 100%"
exit 0