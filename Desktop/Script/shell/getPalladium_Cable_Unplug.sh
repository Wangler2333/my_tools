#!/bin/sh

CableCheck=`system_profiler SPDisplaysDataType | grep -c "PALLADIUM"`
#echo "$CableCheck"

while [ "$CableCheck" -ne 0 ]
do
	echo "Cable not un-plug, pls disconnect it !!!"
	sleep 1
	CableCheck=`system_profiler SPDisplaysDataType | grep -c "PALLADIUM"`
done

echo "Cable un-plug,OK to continue !!!"

exit 0