#/bin/sh


/TE_Support/Scripts/Test_Process/checkBatCap.sh -l 0 -u 85

if [ $? -ne 0 ];then
osascript -e 'tell application "System Events"' -e 'keystroke "t" using command down' -e  'keystroke "/Library/Frameworks/ADStressTools.framework/Resources/VertexPerformanceTest/vertexperf -r 14400 -t0 -t1 -t2 -c -s -m -p quadStrip -M drawArraysWithStaticVBO -A -w 600 -h 600 -b -d 25 -avg -b &"' -e 'keystroke return' -e 'end tell'
fi

/TE_Support/Scripts/Test_Process/checkBatCap.sh -l 0 -u 85
response=$?

while [ $response -ne 0 ]
do

/TE_Support/Scripts/Test_Process/checkBatCap.sh -l 0 -u 85
response=$?

echo "checking battery cap ... "

sleep 3

done

killall -m vertexperf
sleep 1

reboot