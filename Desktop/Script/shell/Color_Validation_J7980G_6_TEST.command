#!/bin/sh

killall Optikos
#/usr/local/bin/hidreport -pid 0x278 -interface 1 -type output set 0xB0 0xB0 0x01 0x00 0x20 0x00 0x00
#sleep 1
#/usr/local/bin/hidreport -pid 0x278 -interface 1 -type output set 0xB0 0xB0 0x01 0x00 0x00 0x00 0x00

rm -rf /Phoenix/Logs/BanksiaLRR_R.txt   ## This is to simulate TCON corruption situation



echo "Validate. Gamma_2 Measure.\n"
/Phoenix/Tools_display/Optikos.app/Contents/MacOS/Optikos --measurementType CAS140 --sequence --saveMeasurementFile /Phoenix/Logs/GAMMA_2 --colorSource sRGB --step verification --mode production --gamma --dfrWhitePoint --promptColor red --ethernetStabilizationWaitTime 0
DWCl_Rslt=$?
echo "DWCl_Rslt"
echo $DWCl_Rslt
if ([ $DWCl_Rslt -ne 0 ]); then
	echo "DWCl_Rslt_Failed"
fi

/Phoenix/Tools_display/brightc --d 0 --s 1

echo "Gamma_2 Validation....\n"
/Phoenix/Tools_display/Optikos.app/Contents/MacOS/Optikos --systemType J5 --validateGamma /Phoenix/Logs/GAMMA_2
GAMMA_Rslt=$?
echo "GMMA_Rslt"
echo $GAMMA_Rslt
if ([ $GAMMA_Rslt -ne 0 ]); then
	echo "GMMA_Failed"
fi

sleep 0.5

echo "WhitePoint Validation....\n"
/Phoenix/Tools_display/Optikos.app/Contents/MacOS/Optikos --systemType J5 --validateWhitePoint /Phoenix/Logs/GAMMA_1 /Phoenix/Logs/GAMMA_2 --commsType ENETComms
WP_Rslt=$?
echo "WP_Rslt"
echo $WP_Rslt
if ([ $WP_Rslt -ne 0 ]); then
	echo "WP_Failed"
fi
sleep 0.5

/Phoenix/Tools_display/Optikos.app/Contents/MacOS/Optikos --parseData /Phoenix/Logs/GAMMA_2 --outputFile /Phoenix/Logs/GAMMA_WP

Rslt=$GAMMA_Rslt+$WP_Rslt+$DWCl_Rslt
echo "GMMA_WP_DWCl_Rslt\n"
echo $Rslt


# Read TCON EEPROM back and check it byte-to-byte
/Phoenix/Tools_display/Optikos.app/Contents/MacOS/Optikos --TconFlashCheck
echo "TCON EEPROM data check \n"
echo $Rslt


sleep 1

/Phoenix/Tools_display/Optikos.app/Contents/MacOS/Optikos --endSession

rm -rf /Phoenix/Logs/ParametricData/Optikos*

exit 0

