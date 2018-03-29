#!/bin/bash

    #systemSN=$(system_profiler | grep "Serial Number (system):" | sed 's/Serial Number (system)://g')
SerNum=`system_profiler SPHardwareDataType | grep "Serial Number" | sed 's/.*: //'`

#systemSN=$(cat /Phoenix/Logs/processlog.plog | grep 'type="System"' | sed 's/^.*serialNumber="//g' | sed 's/".*//g')
    echo -n $SerNum > /Users/saseny/Desktop/SerialNumber.txt

