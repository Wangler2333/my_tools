#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Create by Saseny on 2017/05/26
# Only for box SN Test Check
# For Line Check

import re

def writefile(string, file):
    try:
        with open(file, 'a') as d:
            d.write(string + '\n')
    except IOError as i:
        print ('IOError:', i)

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

def CheckXenon(filename,port):
    with open(filename) as ae:
        try:
            XenonStates = "Y"
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
            print int(len(p)) - 24
            print len(u)
            XenonBox1 = set(p)
            XenonBox = []
            for o in XenonBox1:
                XenonBox.append(o)
            if "Left" in port:
                if len(XenonBox) < 2:
                    XenonStates = "N"
                    if len(SerialCable) > 2:
                        print "\033[0;32m[" + " 测试线未抓到，数据线抓到，确认抓到多个 Serial cable 测试..." + "]\033[0m"
                        print "\033[0;32m[" + " 正常 Flow AAB 测试，请正常打不良.... Thanks! " + "]\033[0m"
                    if len(SerialCable) < 2:
                        print "\033[0;31m[" + " 没有 Flow AAB 操作，请确认.... " + "]\033[0m"
                        print "\033[0;31m[" + " 显示数据线和测试线均未抓到，请确认「 左边 」孔是否无功能....若确认是孔无功能请正常打不良....谢谢！" + "]\033[0m"
                if len(XenonBox) == 2:
                    XenonStates = "Y"
                    print "\033[0;32m[" + " 正常 Flow AAB 测试，请正常打不良.... Thanks! "  + "]\033[0m"
                if len(XenonBox) > 2:
                    XenonStates = "Y"
                    print "\033[0;32m[" + " 正常 Flow AAB 测试，请正常打不良.... Thanks! "  + "]\033[0m"
            if "Right" in port:
                if len(XenonBox) < 3:
                    XenonStates = "N"
                    if len(SerialCable) > 3:
                        print "\033[0;32m[" + " 测试线未抓到，数据线抓到，确认多个Serial cable测试..." + "]\033[0m"
                        print "\033[0;32m[" + " 正常 Flow AAB 测试，请正常打不良.... Thanks! " + "]\033[0m"
                    if len(SerialCable) < 3:
                        print "\033[0;31m[" + " 没有 Flow AAB 操作，请确认.... " + "]\033[0m"
                        print "\033[0;31m[" + " 显示数据线和测试线均未抓到，请确认「 右边 」孔是否无功能....若确认是孔无功能请正常打不良....谢谢！" + "]\033[0m"
                if len(XenonBox) == 3:
                    XenonStates = "Y"
                    print "\033[0;32m[" + " 正常 Flow AAB 测试，请正常打不良.... Thanks! "  + "]\033[0m"
                if len(XenonBox) > 3:
                    XenonStates = "Y"
                    print "\033[0;32m[" + " 正常 Flow AAB 测试，请正常打不良.... Thanks! "  + "]\033[0m"
            print "--->>>"
            print "Box SN: " + str(XenonBox)
            print "Serial Cable: " + str(SerialCable)
        except TypeError as e:
            print('UnboundLocalError', e)

def CheckTBT(filename,port):
    with open(filename) as ae:
        try:
            PalladiumStates = "Y"
            p = []
            for line in ae:
                ps = re.findall(r'FAPP[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]', line)
                if ps:
                    p.append(ps[0])
            Palladium1 = set(p)
            PalladiumBox = []
            for p in Palladium1:
                PalladiumBox.append(p)
            if "Left" in port:
                if len(PalladiumBox) < 2:
                    print "\033[0;31m[" + " 显示数据线和测试线均未抓到，请确认「 左边 」孔是否无功能....若确认是孔无功能请正常打不良....谢谢！" + "]\033[0m"
                if len(PalladiumBox) == 2:
                    PalladiumStates = "N"
                    print "\033[0;31m[" + " 没有 Flow AAB 操作，请确认.... " + "]\033[0m"
                    print "\033[0;31m[" + " 显示数据线和测试线均未抓到，请确认「 左边 」孔是否无功能....若确认是孔无功能请正常打不良....谢谢！" + "]\033[0m"
                if len(PalladiumBox) == 4:
                    PalladiumStates = "Y"
                    print "\033[0;32m[" + " 正常 Flow AAB 测试，请正常打不良.... Thanks! " + "]\033[0m"
                if len(PalladiumBox) > 4:
                    PalladiumStates = "Y"
                    print "\033[0;32m[" + " 正常 Flow AAB 测试，请正常打不良.... Thanks! " + "]\033[0m"
            if "Right" in port:
                if len(PalladiumBox) < 4:
                    PalladiumStates = "N"
                    print "\033[0;31m[" + " 没有 Flow AAB 操作，请确认.... " + "]\033[0m"
                    print "\033[0;31m[" + " 显示数据线和测试线均未抓到，请确认「 右边 」孔是否无功能....若确认是孔无功能请正常打不良....谢谢！" + "]\033[0m"
                if len(PalladiumBox) == 4:
                    PalladiumStates = "N"
                    print "\033[0;31m[" + " 没有 Flow AAB 操作，请确认.... " + "]\033[0m"
                    print "\033[0;31m[" + " 显示数据线和测试线均未抓到，请确认「 右边 」孔是否无功能....若确认是孔无功能请正常打不良....谢谢！" + "]\033[0m"
                if len(PalladiumBox) == 6:
                    PalladiumStates = "Y"
                    print "\033[0;32m[" + " 正常 Flow AAB 测试，请正常打不良.... Thanks! " + "]\033[0m"
                if len(PalladiumBox) > 6:
                    PalladiumStates = "Y"
                    print "\033[0;32m[" + " 正常 Flow AAB 测试，请正常打不良.... Thanks! " + "]\033[0m"
        except TypeError as e:
            print('UnboundLocalError', e)

def CheckDP(filename,port):
    '''
     Waiting Update.....
    :param filename:
    :param port:
    :return:
    '''
    print "DP"

if __name__ == '__main__':
    LogPath = "/Phoenix/Logs/processlog.plog"
    TestBox,Port,Code,SerialNumber,BundleName = CheckSNandBundle(LogPath)
    if "USBPort" in TestBox or "PowerPort" in TestBox:
        print ""
        print "Box info:" + '\t' + "\033[0;34m" + " Xenon Box" + "\033[0m"
        print "Test Item info: "+ '\t' + "\033[0;34m" + Code + ' / ' + Port + "\033[0m"
        print "Test Bundle info: "+ '\t' + "\033[0;34m" + BundleName + "\033[0m" ; print ""
        print "\033[0;33m" + "--->>>" + "\033[0m"
        CheckXenon(LogPath,Port)
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
    #if "VideoPort" in TestBox and "4274" in Code:
    #    CheckDP(LogPath,Port)