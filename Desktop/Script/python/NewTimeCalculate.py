#!/usr/bin/env python
# coding=UTF-8

import time

def Time_chek(_time):
    try:
        timeArray = time.strptime(_time, "%Y/%m/%d %H:%M:%S")
        timeStamp = int(time.mktime(timeArray))
        return timeStamp
    except UnboundLocalError as p:
        print ('UnboundLocalError' ,p)

def Time_calculate(Start ,End):
    d = int(End) - int(Start)
    hour = d / 3600
    d1 = d % 3600
    min = d1 / 60
    d2 = d1 % 60
    time = str(hour) + "h" + str(min) + "m" + str(d2) + "s"
    return time

def TimePlus(Time1,Time2):
    h1 = str(Time1).split('h')[0]
    h2 = str(Time2).split('h')[0]
    m1 = str(Time1).split('m')[0].split('h')[1]
    m2 = str(Time2).split('m')[0].split('h')[1]
    s1 = str(Time1).split('s')[0].split('m')[1]
    s2 = str(Time2).split('s')[0].split('m')[1]
    h = int(h1) + int(h2)
    m = int(m1) + int(m2)
    s = int(s1) + int(s2)
    TIME = str(h) + "h" + str(m) + "m" + str(s) + "s"
    return TIME

def Processing():
    time1 = Time_calculate(Time_chek(Start),Time_chek(Gettime1))
    time2 = Time_calculate(Time_chek(Gettime2),Time_chek(ScanWIP1))
    time3 = Time_calculate(Time_chek(ScanWIP1),Time_chek(ScanWIP2))
    time6 =  Time_calculate(Time_chek(ScanWIP2),Time_chek(ScanWIP3))
    time4 = Time_calculate(Time_chek(ScanWIP3),Time_chek(ScanWIP4))
    time5 = Time_calculate(Time_chek(ScanWIP2),Time_chek(End))

    print "总耗时间：      " + time1 + " " + time2 + " " + time5 + " " + time6
    print "ScanWIP等待时间:" + time3 + " " + time4

if __name__ == '__main__':
    Start = raw_input("Pls input time (Start) : ")
    Gettime1 = raw_input("Pls inout time (GetTime1) : ")
    Gettime2 = raw_input("Pls inout time (Gettime2) : ")
    ScanWIP1 = raw_input("Pls inout time (ScanWIP1) : ")
    ScanWIP2 = raw_input("Pls inout time (ScanWIP2) : ")
    ScanWIP3 = raw_input("Pls inout time (ScanWIP3) : ")
    ScanWIP4 = raw_input("Pls inout time (ScanWIP4) : ")
    End = raw_input("Pls inout time (End) :")
    Processing()
