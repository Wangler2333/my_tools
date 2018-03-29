#!/bin/bash

    if ! [ -d /ALSCalData ]; then
        mkdir /ALSCalData
    fi

    logFile="/Phoenix/Logs/processlog.plog";
    tmpData="/ALSCalData/tmp.txt"

    cameraSerialNumber=$(grep INFO-IDEV $logFile | grep 'class="Camera"' | grep serial-number | sed 's/^.*serial-number="//g' | sed 's/",.*//g')
    timeStamp=$(date "+%Y_%m_%d@%H_%M_%S")
    alsCalData="/ALSCalData/$cameraSerialNumber-$timeStamp.txt"

    grep SNSR $logFile | grep "TEXT-XSTA" | grep fixtureALS | grep -n AlsRatio | sed 's/:context/,/g' | 
        awk -v cameraSN=$cameraSerialNumber -F, '
            {printf cameraSN", " $1", " $3", " $7"," $8"," $9 "\n";}' | 
        sed 's/ts=//g' | sed 's/TEXT=//g' | sed 's/"//g' > $tmpData

    mv $tmpData $alsCalData
    
