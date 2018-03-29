#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Create by Saseny on 2017/06/01
# Check Box Serial Number and Srical Cable number
# Use for check AAB process
# 1.0

'''
    1. Search all Box Serial Number and Serial Cable with this unit tested;
    2. Through the result to check ABB process, judgement the numbers;
    3. The Palladium x2 box test didn't show Serial Cable, so we only through box SN to checked, maybe have risk, Pls carefully and manual judgement;
    4. Maybe have same risk, if you found , pls tell me and modify it, thanks!
'''

import re

XenonCode = ['4098', '4099', '4152', '4367', '4172', '4173', '4378']
PalladiumCode = ['4384','4504']

Message1 = "\033[0;32m[" + " 正常 Flow AAB 测试，请正常打不良.... Thanks! " + "]\033[0m"
Message2 = "\033[0;34m[" + " 显示数据线和测试线均未抓到，请确认孔是否无功能....若确认是孔无功能请正常打不良....谢谢！" + "]\033[0m"
Message3 = "\033[0;31m[" + " 没有 Flow AAB 操作，请确认.... " + "]\033[0m"
Message4 = "\033[0;33m[" + " 测试线未抓到，数据线抓到，确认【Serial cable】测试, 正常 Flow AAB ..." + "]\033[0m"
Message5 = "\033[0;33m[" + " 测试线抓到，数据线未抓到，确认【Serial cable】测试, 正常 Flow AAB ..." + "]\033[0m"

def CheckSNandBundle(filename):
    with open(filename) as af:
        try:
            a = []
            d = []
            SerialNumber = "None"
            BundleName = "None"
            for line in af:
                if "FAIL-UPDA" in line:
                    a.append(line)
                f = re.findall(r'C02.*\+.*\,',line)
                if f:
                    SerialNumber = f[0].split('+')[0]
                b = re.findall(r'J79A_.*_[0-9]-[0-9]_[0-9]\..*\,',line)
                if b:
                    BundleName = b[0].split('"')[0]
            o = re.findall(r'Extended_Code=\"[0-9][0-9][0-9][0-9]\"',a[-1])
            if o:
                d.append(o[0])
            b = re.findall(r'identifier=\'.*\' & type =\'.*\'', a[-1])
            Code = o[0].split('\"')[1]
            Box = b[0].split('\'')[3]
            Port = b[0].split('\'')[1]
            return Box,Port,Code,SerialNumber,BundleName
        except TypeError as e:
            print('UnboundLocalError', e)

def CheckXenon(filename,port,code):
    with open(filename) as ae:
        try:
            p = []
            u = []
            for line in ae:
                xs = re.findall(r'FAPX[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]', line)
                if xs:
                    p.append(xs[0])
                serialcable = re.findall(r'cu.usbserial-X.*\"', line)
                if serialcable:
                    u.append(serialcable[0].split('"')[0])
            SerialCable1 = set(u)
            SerialCable = []
            for l in SerialCable1:
                SerialCable.append(l)
            XenonBox1 = set(p)
            XenonBox = []
            for o in XenonBox1:
                XenonBox.append(o)
            if port == "Rear Left":
                if code == "4098":
                    if len(SerialCable) == 0 and len(XenonBox) == 0:
                        print Message2
                    if len(SerialCable) > 1:
                        if len(XenonBox) == 0:
                            print Message4
                    if len(SerialCable) == 1 and len(u) > 1:
                            print Message3
                    if len(SerialCable) > 1 and len(XenonBox) > 1:
                        print Message1
                    if len(XenonBox) >= 2:
                        print Message1
                if code == "4099":
                    if len(SerialCable) == 1 and len(u) > 2:
                        print Message3
                    if len(SerialCable) > 1:
                        if len(u) > 2 and len(XenonBox) == 1:
                            print Message4
                    if len(u) < 3 and len(XenonBox) < 2:
                        print Message2
                    if len(SerialCable) >= 2 and len(u) >= 3:
                        print Message1
                if code == "4152" or code == "4367":
                    if len(XenonBox) == 1:
                        print Message3
                    if len(XenonBox) > 1:
                        print Message1
                if code == "4172":
                    if len(SerialCable) == 1 and len(u) > 4:
                        print Message3
                    if len(SerialCable) > 1 and len(u) > 4:
                        if len(XenonBox) == 1:
                            print Message4
                        if len(XenonBox) > 1:
                            print Message1
                    if len(SerialCable) == 1 and len(u) == 4:
                        print Message2
                if code == "4173":
                    if len(SerialCable) == 1 and len(u) > 6:
                        print Message3
                    if len(SerialCable) > 1 and len(u) > 6:
                        if len(XenonBox) == 1:
                            print Message4
                        if len(XenonBox) > 1:
                            print Message1
                    if len(SerialCable) == 1 and len(u) == 6:
                        print Message2
            if port == "Front Left":
                if code == "4098":
                    if len(SerialCable) == 1 and len(u) > 8:
                        print Message3
                    if len(SerialCable) > 1 and len(u) > 8:
                        if len(XenonBox) == 1:
                            print Message4
                        if len(XenonBox) > 1:
                            print Message1
                    if len(SerialCable) == 1 and len(u) == 8:
                        print Message2
                if code == "4099":
                    if len(SerialCable) == 1 and len(u) > 10:
                        print Message3
                    if len(SerialCable) > 1 and len(u) > 10:
                        if len(XenonBox) == 1:
                            print Message4
                        if len(XenonBox) > 1:
                            print Message1
                    if len(SerialCable) == 1 and len(u) == 10:
                        print Message2
                if code == "4152" or code == "4367":
                    if len(XenonBox) == 1:
                        print Message3
                    if len(XenonBox) > 1:
                        print Message1
                if code == "4378":
                    if len(XenonBox) == 1:
                        print Message3
                    if len(XenonBox) > 1:
                        print Message1
                if code == "4172":
                    if len(SerialCable) == 1 and len(u) > 12:
                        print Message3
                    if len(SerialCable) > 1 and len(u) > 12:
                        if len(XenonBox) == 1:
                            print Message4
                        if len(XenonBox) > 1:
                            print Message1
                    if len(SerialCable) == 1 and len(u) == 12:
                        print Message2
                if code == "4173":
                    if len(SerialCable) == 1 and len(u) > 14:
                        print Message3
                    if len(SerialCable) > 1 and len(u) > 14:
                        if len(XenonBox) == 1:
                            print Message4
                        if len(XenonBox) > 1:
                            print Message1
                    if len(SerialCable) == 1 and len(u) == 14:
                        print Message2
            if port == "Rear Right":
                if code == "4098":
                    if len(SerialCable) == 1 and len(u) > 16:
                        print Message3
                    if len(SerialCable) == 1 and len(u) == 16 and len(XenonBox) == 1:
                        print Message2
                    if len(SerialCable) == 2 and len(u) > 16:
                        print Message3
                    if len(SerialCable) > 2 and len(u) > 16:
                        if len(XenonBox) == 1:
                            print Message4
                        if len(XenonBox) >= 2:
                            print Message1
                    if len(XenonBox) == 2 and len(u) == 16 and len(SerialCable) == 1:
                        print Message5
                    if len(XenonBox) >2:
                        print Message5
                if code == "4099":
                    if len(SerialCable) == 2 and len(u) > 18:
                        print Message3
                    if len(SerialCable) > 2 and len(u) > 18:
                        if len(XenonBox) == 2:
                            print Message4
                        if len(XenonBox) > 2:
                            print Message1
                    if len(SerialCable) == 2 and len(u) == 18:
                        print Message2
                if code == "4152" or code == "4367":
                    if len(XenonBox) == 2:
                        print Message3
                    if len(XenonBox) > 2:
                        print Message1
                if code == "4172":
                    if len(SerialCable) == 2 and len(u) > 20:
                        print Message3
                    if len(SerialCable) > 2 and len(u) > 20:
                        if len(XenonBox) == 2:
                            print Message4
                        if len(XenonBox) > 2:
                            print Message1
                    if len(SerialCable) == 2 and len(u) == 20:
                        print Message2
                if code == "4173":
                    if len(SerialCable) == 2 and len(u) > 22:
                        print Message3
                    if len(SerialCable) > 2 and len(u) > 22:
                        if len(XenonBox) == 2:
                            print Message4
                        if len(XenonBox) > 2:
                            print Message1
                    if len(SerialCable) == 2 and len(u) == 22:
                        print Message2
                if code == "4378":
                    if len(XenonBox) == 2:
                        print Message3
                    if len(XenonBox) > 2:
                        print Message1
            if port == "Front Right":
                if code == "4098":
                    if len(SerialCable) == 2 and len(u) > 24:
                        print Message3
                    if len(SerialCable) > 2 and len(u) > 24:
                        if len(XenonBox) == 2:
                            print Message4
                        if len(XenonBox) > 2:
                            print Message1
                    if len(SerialCable) == 2 and len(u) == 24:
                        print Message2
                if code == "4099":
                    if len(SerialCable) == 2 and len(u) > 26:
                        print Message3
                    if len(SerialCable) > 2 and len(u) > 26:
                        if len(XenonBox) == 2:
                            print Message4
                        if len(XenonBox) > 2:
                            print Message1
                    if len(SerialCable) == 2 and len(u) == 26:
                        print Message2
                if code == "4152" or code == "4367":
                    if len(XenonBox) == 2:
                        print Message3
                    if len(XenonBox) > 2:
                        print Message1
                if code == "4172":
                    if len(SerialCable) == 2 and len(u) > 28:
                        print Message3
                    if len(SerialCable) > 2 and len(u) > 28:
                        if len(XenonBox) == 2:
                            print Message4
                        if len(XenonBox) > 2:
                            print Message1
                    if len(SerialCable) == 2 and len(u) == 28:
                        print Message2
                if code == "4173":
                    if len(SerialCable) == 2 and len(u) > 30:
                        print Message3
                    if len(SerialCable) > 2 and len(u) > 30:
                        if len(XenonBox) == 2:
                            print Message4
                        if len(XenonBox) > 2:
                            print Message1
                    if len(SerialCable) == 2 and len(u) == 30:
                        print Message2
                if code == "4378":
                    if len(XenonBox) == 2:
                        print Message3
                    if len(XenonBox) > 2:
                        print Message1
            print "--->>>"
            print "Box SN: {" + str(len(XenonBox)) + '} | ' + str(XenonBox)
            print "Serial Cable: {" + str(len(SerialCable)) + '} | ' + str(SerialCable)
            print len(u)
        except TypeError as e:
            print('UnboundLocalError', e)

def CheckTBT(filename,port):
    with open(filename) as ae:
        try:
            p = []
            for line in ae:
                ps = re.findall(r'FAPP[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]', line)
                if ps:
                    p.append(ps[0])
            Palladium1 = set(p)
            PalladiumBox = []
            for p in Palladium1:
                PalladiumBox.append(p)
            if port == "Rear Left":
                if len(PalladiumBox) == 0:
                    print Message2
                if len(PalladiumBox) == 2:
                    print Message3
                if len(PalladiumBox) > 2:
                    print Message1
            if port == "Front Left":
                if len(PalladiumBox) == 2:
                    print Message3
                if len(PalladiumBox) > 2:
                    print Message1
            if port == "Rear Right":
                if len(PalladiumBox) == 2:
                    print Message2
                if len(PalladiumBox) == 4:
                    print Message3
                if len(PalladiumBox) > 4:
                    print Message1
            if port == "Front Right":
                if len(PalladiumBox) == 4:
                    print Message3
                if len(PalladiumBox) > 4:
                    print Message1
            print "--->>>"
            print "Box SN: {" + str(len(PalladiumBox)) + '} | ' +  str(PalladiumBox)
        except TypeError as e:
            print('UnboundLocalError', e)

if __name__ == '__main__':
    LogPath = "/Phoenix/Logs/processlog.plog"
    TestBox, Port, Code, SerialNumber, BundleName = CheckSNandBundle(LogPath)
    if "USBPort" in TestBox or "PowerPort" in TestBox:
        print ""
        print "Box info:" + '\t' + "\033[0;34m" + " Xenon Box" + "\033[0m"
        print "Test Item info: "+ '\t' + "\033[0;34m" + Code + ' / ' + Port + "\033[0m"
        print "Test Bundle info: "+ '\t' + "\033[0;34m" + BundleName + "\033[0m" ; print ""
        print "\033[0;33m" + "--->>>" + "\033[0m"
        CheckXenon(LogPath,Port,Code)
        print ""
    if "ThunderboltPort" in TestBox:
        print ""
        print "Box info:" + '\t' + "\033[0;34m" + " Palladium Box" + "\033[0m"
        print "Test Item info: "+ '\t' + "\033[0;34m" + Code + ' / ' + Port + "\033[0m"
        print "Test Bundle info: "+ '\t' + "\033[0;34m" + BundleName + "\033[0m" ; print ""
        print "\033[0;33m" + "--->>>" + "\033[0m"
        CheckTBT(LogPath,Port)
        print ""
    if "VideoPort" in TestBox and "4504" in Code:
        print ""
        print "Box info:" + '\t' + "\033[0;34m" + " Palladium Box" + "\033[0m"
        print "Test Item info: "+ '\t' + "\033[0;34m" + Code + ' / ' + Port + "\033[0m"
        print "Test Bundle info: "+ '\t' + "\033[0;34m" + BundleName + "\033[0m" ; print ""
        print "\033[0;33m" + "--->>>" + "\033[0m"
        CheckTBT(LogPath,Port)
        print ""