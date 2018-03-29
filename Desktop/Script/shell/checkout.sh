#!/bin/sh

Connect=`system_profiler SPUSBDataType | grep -c "Apple USB Ethernet Adapter"`

A=`ls /Users/saseny/Desktop | grep -c "zero.sh"`
while [ $A -eq 0 ]
do 
echo " No File at Desktop, so we need check it why"
sleep 1

A=`ls /Users/saseny/Desktop | grep -c "zero.sh"`

sleep 1
done

diskutil list
sleep 5



while [ ! -f /Users/saseny/Desktop/zero.sh ]
do 
echo " no........no.......no.......no.......no........no........no  "
sleep 1

done

cal