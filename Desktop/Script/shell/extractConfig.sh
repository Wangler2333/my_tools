#!/bin/bash

    logFolder="/Phoenix/Logs/"
    logFileName="$logFolder/processlog.plog"    
    configFileName="$logFolder/extractedConfig.txt"    
    

mapMemVendor(){
    if [ $1 == "0x80CE" ]; then
       memVendor="Samsung"
    elif [ $1 == "0x80AD" ]; then
       memVendor="Hynix"
    elif [ $1 == "0x802C" ]; then
       memVendor="Micron"
    elif [ $1 == "0x8551" ]; then
       memVendor="Qimonda"
    elif [ $1 == "0x830B" ]; then
       memVendor="Nanya"
    elif [ $1 == "0x02FE" ]; then
       memVendor="Elpida"
    else
       memVendor="Unknown($1)"
    fi
}

    panelVendor=$(grep DISP $logFileName | grep "TEXT-XSTA" | grep "Panel" | tail -1 | 
            awk '{print $NF}' | sed 's/\"//g')
    tconVendor=$(grep DISP $logFileName | grep "TEXT-XSTA" | grep "TCON" | tail -1 | 
            awk '{print $NF}' | sed 's/\"//g')
    cpuSpeed=$(grep INFO-IDEV $logFileName | grep 'class="Processor"' | tail -1 | 
            sed 's/^.*,vendor=\"\(.*\)",family.*\,max-speed=\"\(.*\)",fsb-speed.*/\1 \2/g')
    memVendorCode=$(grep INFO-IDEV $logFileName | grep 'class="Memory"' | grep 'location' | tail -1 | 
            sed 's/^.*,vendor=\"\(.*\)",serial.*/\1/g')
    mapMemVendor $memVendorCode
    memSize=$(grep INFO-IDEV $logFileName | grep 'class="Memory"' | grep 'type="virtual"' | tail -1 | 
            sed 's/^.*,size=\"\(.*\)",max-devices=\"\(.*\)",is-ecc.*/\1 (\2x Banks)/g')
    ssdVendorSize=$(grep INFO-IDEV $logFileName | grep 'class="HardDrive"' | tail -1 | 
            sed 's/^.*,type=\"\(.*\)",location.*\,vendor=\"\(.*\)",model.*capacity=\"\(.*\)\",size.*,version=\"\(.*\)",bsd.*/\2 \1 \3 (\4)/g')
    keyboard=$(grep INFO-IDEV $logFileName | grep 'class="Keyboard"' | tail -1 | 
            sed 's/^.*,country=\"\(.*\)",type.*firmware-version=\"\(.*\)".*/\1 (ver\2)/g')
    trackpad=$(grep INFO-IDEV $logFileName | grep 'class="Pointer"' | tail -1 | 
            sed 's/^.*,model=\"\(.*\)",version.*firmware-version=\"\(.*\)",Z2-firmware-version=\"\(.*\)",open.*/\1 (PSOC \2 \/ Z2 \3)/g')
    airport=$(grep INFO-IDEV $logFileName | grep 'class="AirPort"' | tail -1 | 
            sed 's/^.*,vendor=\"\(.*\)",model=\"\(.*\)",firmware-version=\"\(.*\)",driver-version=\"\(.*\),location.*country=\"\(.*\)\",locale.*/\2(Country \5)/g')
    bluetooth=$(grep INFO-IDEV $logFileName | grep 'class="Bluetooth"' | tail -1 | 
            sed 's/^.*,vendor=\"\(.*\)",model=\"\(.*\)",mac-address.*,version=\"\(.*\)",firmware-version.*/\2(\3)/g')
          
    if [ -f $configFileName ]; then
        rm $configFileName
    fi
    echo "CPU:          $cpuSpeed" >> $configFileName
    echo "Memory:       $memVendor $memSize" >> $configFileName
    echo "SSD:          $ssdVendorSize" >> $configFileName
    echo "Keyboard:     $keyboard" >> $configFileName
    echo "Trackpad:     $trackpad" >> $configFileName
    echo "Bluetooth:    $bluetooth" >> $configFileName
    echo "Airport:      $airport" >> $configFileName
    echo "Panel:        $panelVendor" >> $configFileName
    echo "TCon:         $tconVendor" >> $configFileName
    
    cp $configFileName /var/tmp/extractedConfig.txt

    open /var/tmp/extractedConfig.txt
