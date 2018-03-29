#!/usr/bin/python
# -*- coding: UTF-8 -*-

from subprocess import Popen, PIPE
from plistlib import readPlistFromString

Dic = {"C02TJ002HT7N":"Thai","C02TJ001HT7N":"Thai","C02TJ001HW6R":"Spanish - ISO","C02TJ002HW6R":"Russian","C02TJ001HW6T":"Japanese Keyboard","C02S60L1G8WP":"2"}
ConfigFile="/Phoenix/Configuration/configExpected.txt"

def systemProfiler(types):
    systemProfilerXml=Popen(["system_profiler", types, "-xml"], stdout=PIPE).communicate()[0]
    pl=readPlistFromString(systemProfilerXml)
    return pl

def SP(types,item_to_check):
    return systemProfiler(types)[0]['_items'][0][item_to_check]

def ConfigFileCheck():
    with open(ConfigFile) as ie:
        #txt = ie.read()
        for line in ie:
            if "Keyboard" in line and "language" in line:
                print line


SerialNumber = SP("SPHardwareDataType",'serial_number')
print SerialNumber

for i in dict.keys(Dic):
    if SerialNumber == i:
        print Dic[SerialNumber]

ConfigFileCheck()

