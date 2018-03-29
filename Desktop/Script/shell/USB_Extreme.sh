
#Right Rear:Extreme@01300000
#Right Front:Extreme@01400000
#Left Rear: Extreme@00400000
#Left Front: Extreme@00300000 

string=$1

case $string in
"RR" )
grepString="Extreme@01300000"
theString="Right Rear"
;;
"RF" )
grepString="Extreme@01400000"
theString="Right Front"
;;
"LR" )
grepString="Extreme@00400000"
theString="Left Rear"
;;
"LF" )
grepString="Extreme@00300000"
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



