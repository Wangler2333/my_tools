#!/bin/sh
/usr/local/bin/ypc2 -w MSLD 02
killall WiPASminiOSX
echo ota.tethering.method=scorpio > /Applications/WiPAS/boot-args.txt;
mkdir -p /Phoenix/Logs/WiPAS/
/Applications/WiPAS/WiPASminiOSX.app/Contents/MacOS/WiPASminiOSX -c standalone -l stdout >> /Phoenix/Logs/WiPAS/WiPASminiTerminal.txt 2>&1 &
tail -n 1000 -F /Phoenix/Logs/WiPAS/WiPASminiTerminal.txt
