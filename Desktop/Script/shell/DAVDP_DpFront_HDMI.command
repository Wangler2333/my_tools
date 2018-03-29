#!/bin/sh

testName=$1

case $testName in
"frontdp" )
RomToCheck=44502d48444d492041444150544f5204a0001cf8505338343032a20000780f00
dongle="Front DP"
;;
"hdmi" )
RomToCheck=44502d48444d492041444150544f5204a00010fa6848444d4961100000780f00
dongle="HDMI"
;;
esac

DongleROM=`ioreg -lw0 | grep IOFBHDMIDongleROM | sed 's/.*= //' | sed 's/<//' | sed 's/>//'`

if [ "$DongleROM" != "$RomToCheck" ];then
echo "Wrong dongle use!"
echo "Expected $dongle"
exit 1
else 
echo "Pass, correct dongle use!"
exit 0
fi