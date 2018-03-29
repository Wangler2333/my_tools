#!/bin/sh
#1.0
#SN=`cat /Phoenix/Logs/SerialNumber.txt`

#NYCPN=`cat /Phoenix/Logs/processlog.plog | grep "WIP scanned=" | cut -d "=" -f 2 | awk '{print $1}'`
NYCPN=`cat /Phoenix/Logs/processlog.plog | grep -m 1 -o 'WIP scanned=".*"' | cut -f2 -d"+" | cut -f1 -d '"'`

#echo "$SN"
#echo "$KSN"

if [ "${NYCPN}" == "K0QM1LL/A" ] || [ "${NYCPN}" == "K0QN0LL/A" ] || [ "${NYCPN}" == "K0QN2LL/A" ];then
echo "$NYCPN is NYC model,PASS"
exit 0
else
echo "$NYCPN is Not NYC model,pls re-download with normal bundle"
exit 1
fi