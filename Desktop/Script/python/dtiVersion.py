#!/usr/bin/env python
import os
import datetime
import time
import datetime
import csv

from subprocess import Popen, PIPE, check_output
from plistlib import readPlistFromString, readPlist
from pprint import pprint
from commands import *

compare_flag = False
match_flag = False

def systemProfiler(types):
    systemProfilerXml=Popen(["system_profiler", types, "-xml"], stdout=PIPE).communicate()[0]
    pl=readPlistFromString(systemProfilerXml)
    return pl

def SP(types,item_to_check):
    return systemProfiler(types)[0]['_items'][0][item_to_check]

def run(cmd):
    status=getstatusoutput(cmd)
    print status

def writefile(string):
    with open(outputfile, 'a') as f:
        f.write(string + '\n')
        
        
    
'''------------'''
''' Initialize ''' 
'''------------'''
now = datetime.datetime.now()
cTime = now.strftime("%Y_%m_%d_%H_%M_%S")

currentPath=os.getcwd()
currentFilePath=os.path.dirname(os.path.abspath(__file__)) 
pluginPath="/AppleInternal/Diagnostics/OS/Plugins/"
frameworkPath="/Library/Frameworks/"
kextPath="/System/Library/Extensions/"

firstDTI = currentFilePath + '/dti.csv'
if os.path.isfile(firstDTI):
    print "[File Check] Current Dti file exist, archieve original file and compare"
    secondDTI = "%s/dti_%s.csv" % (currentFilePath, cTime)
    os.rename(firstDTI, secondDTI)
    diffFile = "%s/diff.csv" % currentFilePath
    outputfile=firstDTI
    compare_flag = True
    
else:
    print "[File Check] Current Dti file not exist, create dti.txt file"
    outputfile=firstDTI
    compare_flag = False
    


OS_version=SP("SPSoftwareDataType", 'os_version')
Model_version=SP("SPHardwareDataType", 'machine_model')
BootRom_version=SP("SPHardwareDataType", 'boot_rom_version')
SMC_version=SP("SPHardwareDataType", 'SMC_version_system')
Tbt_version=SP("SPThunderboltDataType", 'switch_version_key')
#Trackpad_version=SP("SPSPIDataType", 'c_bcd_device')
AirPort_version=systemProfiler("SPAirPortDataType")[0]['_items'][0]['spairport_airport_interfaces'][0]['spairport_wireless_firmware_version']
Bluetooth_version=systemProfiler("SPBluetoothDataType")[0]['_items'][0]["local_device_title"]['general_fw_version']


print "***DTI Information**************************"
BoardId=os.system('ioreg -l|grep "board-id" |awk \'{print substr($4,3,length($4)-4)}\'')
print "OS version:\t%s" % OS_version
print "Model version:\t%s" % Model_version
print "BootRom:\t%s" % BootRom_version
print "SMC version:\t%s" % SMC_version
print "BT Firmware:\t%s" % Bluetooth_version
print "TBT Firmware:\t%s" % Tbt_version
print "Broadcom driver:\t%s" % AirPort_version
#print "Trackpad version:\t%s" % Trackpad_version
print "*********************************************"

#writefile("DTI Information:")
writefile("OS version;%s" % OS_version)
writefile("Model version;%s" % Model_version)
writefile("Mac - Id;%s" % BoardId)
writefile("BootRom;%s" % BootRom_version)
writefile("SMC version;%s" % SMC_version)
writefile("BT Firmware;%s" % Bluetooth_version)
writefile("TBT Firmware;%s" % Tbt_version)
writefile("Broadcom Firmware;%s" % AirPort_version)
#writefile("Trackpad version;%s" % Trackpad_version)


writefile("***Plugin***;*")
pluginFiles=os.listdir(pluginPath)
for pfile in pluginFiles:
    if pfile.endswith(".plugin"):
        thePluginFilePlist = pluginPath + pfile + '/Contents/Info.plist'
        
        if os.path.isfile(thePluginFilePlist):
            try:
                info = readPlist(thePluginFilePlist)
                thePluginVersion = info['CFBundleShortVersionString']
                writefile("%s;%s" % (pfile,thePluginVersion))        
            except:
                print "Error!!"
                writefile("%s;%s" % (pfile,"ERROR"))

                
writefile("***Framework***;*")
frameworkFiles=os.listdir(frameworkPath)
for ffile in frameworkFiles:
    if ffile.endswith(".framework"):
        theFrameworkFilePlist = frameworkPath + ffile + '/Versions/A/Resources/Info.plist'
        
        if os.path.isfile(theFrameworkFilePlist):
            try:
                infoFrame = readPlist(theFrameworkFilePlist)
                theFrameworkVersion = infoFrame['CFBundleShortVersionString']
                writefile("%s;%s" % (ffile,theFrameworkVersion))
            except:
                writefile("%s;%s" % (ffile,"ERROR"))

writefile("***Kext***;*")
kextFiles=os.listdir(kextPath)
for kfile in kextFiles:
    if kfile.endswith(".kext"):
        theKextFilePlist = kextPath + kfile + '/Contents/Info.plist'
        
        if os.path.isfile(theKextFilePlist):
            infoKext = readPlist(theKextFilePlist)
            theKextVersion = infoKext['CFBundleVersion']
            writefile("%s;%s" % (kfile,theKextVersion))


if compare_flag == True:
    file1 = file(firstDTI, 'r')
    file2 = file(secondDTI, 'r')
    
    delta = "%s/changes.csv" % currentFilePath
    outputfile = delta
    
    incsv_file1 = csv.reader(file1, delimiter=';')
    incsv_file2 = csv.reader(file2, delimiter=';')          
    
    masterlist_file1 = list(incsv_file1)
    print "Dti Changes:\n" 
    m=0
    n=0
    for row in incsv_file2:
        n=n+1
        m=0
        match_flag = False
        for new_row in masterlist_file1:
            m=m+1
            if row[0] == new_row[0]:
                match_flag = True
                if row[1] != new_row[1]:
                    print "%s ; old: [%s] ; new: [%s]" % (row[0], row[1], new_row[1])
                    writefile("%s ; old: [%s] ; new: [%s]" % (row[0], row[1], new_row[1])) 
                break
            else:
                match_flag == False

        if match_flag == False:
            print "%s is missing from new dti" % row[0]
    
    print "=============================="
    print "Total of new dti file: %d" % m 
    print "Total of old dti file: %d" % n  
    print "=============================="
            
