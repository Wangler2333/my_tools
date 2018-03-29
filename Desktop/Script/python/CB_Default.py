#!/usr/bin/python
# -*- coding: UTF-8 -*-

import plistlib
import os,sys
import sipconfig


#Dic = {'Preburn':{'HD-Rack':['0','0x00'],'WIFI-COND':['26','0x1A'],'PREBURN':['234','0xEA'],'FORCE_CAL':['235','0xEB'],'ActuationCAL':['236','0xEC'],'FACT':['163','0xA3'],'Button Test':['219','0xDB'],'WIFI BT OTA':['193','0xC1'],'COEX1':['203','0xCB']},'Runin':{'RUN-IN':['238','0xEE']},'Postburn':{'RGBW':['166','0xA6'],'FLICKER':['240','0xF0'],'LCD Uniformity':['176','0xB0'],'Display FOS':['138','0x8A'],'Grape Cal/ Test':['137','0x89'],'POSTBURN':['239','0xEF']}}
Dic = {'0':['INIT','INITIALIZING_IP'],'1':['CB Error','CB not PASS'],'2':['CB Error','Write CB to Incomplete'],'3':['PRE_TEST_SEQUENCE','DUT_POSITION_CHECK'],'4':['GREY128_FLICKER','GREY128_PATTERN'],'5':['GREY128_FLICKER','PSR128_MODE_ON'],'6':['GREY128_FLICKER','MEASURE_CA310'],'7':['GREY128_FLICKER','PSR128_MODE_OFF'],'8':['GREY75_FLICKER','GREY75_PATTERN'],'9':['GREY75_FLICKER','PSR75_MODE_ON'],'10':['GREY75_FLICKER','MEASURE_CA310'],'11':['GREY75_FLICKER','PSR75_MODE_OFF'],'12':['CB Error','SET CB PASS']}

print dict.keys(Dic)

#pathroad = os.path.dirname(sys.argv[0]) + '/CB_Default.plist'
pathroad = os.path.dirname(sys.argv[0]) + '/Flicker.plist'
plistlib.writePlist(Dic,pathroad)



