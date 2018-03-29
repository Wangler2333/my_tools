#!/bin/sh

failFlag=0
ipAddress="17.238.65.69 17.238.65.70 17.238.65.73 17.238.65.74 17.238.65.75"
port="8080"
ipAddress=($ipAddress)

totalIpAddress=${#ipAddress[@]}
echo "Total Ip to be checked: $totalIpAddress"

for ((i=0; i<$totalIpAddress; i++))
do

case ${ipAddress[$i]} in
"17.238.65.69" ) serverName="spider cab";;
"17.238.65.70" ) serverName="aloha";;
"17.238.65.73" ) serverName="UCA";;
"17.238.65.74" ) serverName="USS";;
"17.238.65.75" ) serverName="DS";;
esac

`nc -z ${ipAddress[$i]} $port`
succeeded=$?

if [ $succeeded -ne 0 ];then
echo "FAIL: Server [$serverName] - ${ipAddress[$i]} $port not Online"
failFlag=1
fi
done

if [ $failFlag != 0 ];then
echo "Result: Failed to ping JMET server"
exit 1
else
echo "Result: JMET Server are online"
exit 0
fi