#!/bin/sh

echo "Check if T101 is ready.."


cnt=0
while [ 1 ]; do
	cnt=`expr $cnt + 1`
	usbserialcount=`ls /dev/cu* | grep -c usbserial`

	echo "Index: $cnt usbserialcount: $usbserialcount ADAcount: $ADAcount"
	if [ $usbserialcount -ne 1 ]; then
		sleep 1
		if [ $cnt -gt 10 ]; then
			break;
		fi
	else
		echo "T101 is ready"
		exit 0
	fi
done

exit 1
