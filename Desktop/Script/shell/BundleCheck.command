#!/bin/sh
	
ls /694-03021-380.dmg

if [ $? -eq 0 ]; then
	echo "Bundle exists"
	#checker
	exit 0
else
	echo "Bundle not exists"
	checker
	#exit 1
fi

checker
{
    diskutil list 
    
}    