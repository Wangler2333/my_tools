
#Right Rear:USB 3.0 FD@01300000
#Right Front:USB 3.0 FD@01400000
#Left Rear: USB 3.0 FD@00400000
#Left Front: USB 3.0 FD@00300000 

string=$1

case $string in
"RR" )
grepString="USB 3.0 FD@01300000"
theString="Right Rear"
;;
"RF" )
grepString="USB 3.0 FD@01400000"
theString="Right Front"
;;
"LR" )
grepString="USB 3.0 FD@00400000"
theString="Left Rear"
;;
"LF" )
grepString="USB 3.0 FD@00300000"
theString="Left Front"
;;
esac


checkPort=`ioreg -lw0 | grep -c "$grepString"`

if [ "$checkPort" == 0 ];then
echo "FAIL: No USB detected at [$theString]"
exit 1
else
echo "PASS: USB detected at [$theString]"
exit 0
fi



