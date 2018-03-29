#!/usr/bin/python
# -*- coding: UTF-8 -*-
# Created by saseny on 2017/03/21
# Modify on 4/5 , add output bundle name and Memory Vendor , Battery level
# Config Info only check 'configExpected.txt'
# Battery level info check 'battery.log', if log haven't 'battery.log' then no battery level output

import time, datetime
import sys
import os
import shutil
from Tkinter import *

def writefile(string,file):
    try:
        with open(file, 'a') as d:
            d.write(string + '\n')
    except IOError as i:
        print ('IOError_4:',i)

def Check_OutFile(file):
    try:
        if not os.path.isfile(file):
            if lb.selection_includes(0) == True and lb.selection_includes(1) == True:
                title = "序列号, CPU, 运行内存, 固态硬盘, 键盘国别, 开始时间, 结束时间, 用时, Bundle, MemoryVendor, BatteryLevel"
            if lb.selection_includes(0) == True and lb.selection_includes(1) == False:
                title = "序列号, CPU, 运行内存, 固态硬盘, 键盘国别, 开始时间, 结束时间, 用时, Bundle, MemoryVendor"
            if lb.selection_includes(0) == False and lb.selection_includes(1) == True:
                title = "序列号, CPU, 运行内存, 固态硬盘, 键盘国别, 开始时间, 结束时间, 用时, Bundle, BatteryLevel"
            if lb.selection_includes(0) == False and lb.selection_includes(1) == False:
                title = "序列号, CPU, 运行内存, 固态硬盘, 键盘国别, 开始时间, 结束时间, 用时, Bundle"
            writefile(title,file)
    except TypeError as h:
        print ('TypeError_1:',h)
        
def Time_chek(_time):
    try:
        timeArray = time.strptime(_time, "%Y/%m/%d %H:%M:%S")
        timeStamp = int(time.mktime(timeArray))
        return timeStamp
    except UnboundLocalError as p:
        print ('UnboundLocalError',p)        
        
def Time_calculate(Start,End):
    d = int(End) - int(Start)
    hour = d / 3600
    d1 = d % 3600
    min = d1 / 60
    d2 = d1 % 60
    time = str(hour) + "h" + str(min) + "m" + str(d2) + "s"
    return time

def check_Memory_vonder(filepath):
    try:
        c = []
        with open(filepath) as gs:
            for line in gs:
                if "Memory" in line and "vendor:" in line:
                    c.append(line.split('"')[11].split(':')[-1])
            return str(c[0])
    except IOError as oi:
        print ('IOError',oi)
    
def find_file(path,formet):
    try:
        fns = [os.path.join(root, fn) for root, dirs, files in os.walk(path) for fn in files]
        for f in fns:
            if os.path.isfile(f):
                if formet in f:
                    return f
    except IOError as o:
        print ('IOError',o)
        
def read_plog(filepath,fromt):
    try:
        a = []
        with open(filepath) as msg:
            for line in msg:
                if fromt in line:
                    a.append(line.split('"')[3])
            TIME = a[0]
            return TIME
    except UnboundLocalError as o:
        print ('UnboundLocalError',o)    

def Bundle_Check(file):
    try:
        b = []
        with open(file) as sg:
            for line in sg:
                if "DTI" in line:
                    ad = line.split('"')[15]
                    b.append(ad)
            return b[1]
    except IOError as f:
        print ('IOError_3:',f)

def check_Battery(filepath):
    try:
        c = []
        with open(filepath) as oi:
            for line in oi:
                if "InternalBattery" in line:
                    c.append(line.split()[2].replace(';',''))
            return c[1]
    except IOError as pp:
        print ('IOError',pp)

def config_check(path):
    try:
        K = "Apple Internal Keyboard / Trackpad"
        with open(path) as fe:
            for line in fe:
                if K in line:
                    KB = line.split('"')[3]
                if "Memory" in line:
                    MY = line.split('"')[1]
                if "devicecapacity" in line:
                    SD = line.split('"')[1]
                    if SD == 1000:
                        SD = 1024
                if "frequency" in line:
                    CPU = line.split('"')[3]
            return  CPU, MY, SD, KB
    except TypeError as po:
        print ('TypeError',po)

def ProcessLog(path,fromt,Check_Start,Check_End):
    Date = time.strftime("%Y_%m_%d_%H_%M_%S")
    resultpath = os.path.expanduser('~') + "/Downloads/" + Date + '.csv'
    ne = 0
    fns = [os.path.join(root, fn) for root, dirs, files in os.walk(path) for fn in files]
    for f in fns:
        if os.path.isfile(f):
            if fromt in f:
                ne = ne + 1
                print >> sys.stdout, "Processing " + str(ne)
                #sys.stdout.flush()
                try:
                    if "PASS" in f or "FAIL" in f:
                        SerialNubmer = os.path.basename(f).split('_')[0]
                        Temproad = os.path.expanduser('~') + "/Downloads/temp"
                        os.system('mkdir -p ~/Downloads/temp')
                        shutil.copy(f,Temproad)
                        os.system('sleep 1')
                        os.system('cd ~/Downloads/temp; tar -xzf * &>/dev/null')

                        ConfigFile = find_file(Temproad,"configExpected.txt")
                        CPU, Memory, SSD, Keyboard = config_check(ConfigFile)

                        plogPath = find_file(Temproad,".plog")

                        A = read_plog(plogPath,Check_Start)
                        B = read_plog(plogPath,Check_End)
                        Bundle = Bundle_Check(plogPath)

                        Startime = Time_chek(read_plog(plogPath,Check_Start))
                        Endtime = Time_chek(read_plog(plogPath,Check_End))
                        Time = Time_calculate(Startime, Endtime)
                        ao = str(SerialNubmer) + "," + str(CPU) + "," + str(Memory) + "," + str(SSD) + "," + str(Keyboard)

                        if lb.selection_includes(0) == True and lb.selection_includes(1) == True:
                            Memory_vendor = check_Memory_vonder(plogPath)
                            Battery_Level = check_Battery(find_file(Temproad,"battery.log"))
                            ap = str(A) + "," + str(B) + "," + str(Time) + "," + str(Bundle) + "," + str(Memory_vendor) + "," + str(Battery_Level)
                            result_ = ao + "," + ap
                        if lb.selection_includes(0) == True and lb.selection_includes(1) == False:
                            Memory_vendor = check_Memory_vonder(plogPath)
                            ap = str(A) + "," + str(B) + "," + str(Time) + "," + str(Bundle) + "," + str(Memory_vendor)
                            result_ = ao + "," + ap
                        if lb.selection_includes(0) == False and lb.selection_includes(1) == True:
                            Battery_Level = check_Battery(find_file(Temproad, "battery.log"))
                            ap = str(A) + "," + str(B) + "," + str(Time) + "," + str(Bundle) + "," + str(Battery_Level)
                            result_ = ao + "," + ap
                        if lb.selection_includes(0) == False and lb.selection_includes(1) == False:
                            ap = str(A) + "," + str(B) + "," + str(Time) + "," + str(Bundle)
                            result_ = ao + "," + ap

                        writefile(result_,resultpath)
                        shutil.rmtree(Temproad)
                        if os.path.isdir(Temproad):
                            shutil.rmtree(Temproad)

                except TypeError as op:
                    if os.path.isdir(Temproad):
                        shutil.rmtree(Temproad)
                    print ('TypeError',op)

def btn_click():

    if e2.get() == "":
        Check_Start = "CM_Bundle_Verify"
    else:
        Check_Start = e2.get()
    if e3.get() == "":
        Check_End = "Color_Cal_J79_0_native_flash"
    else:
        Check_End = e3.get()

    evalue = e1.get()

    Temproad = os.path.expanduser('~') + "/Downloads/temp"
    Date = time.strftime("%Y_%m_%d_%H_%M_%S")
    resultpath = os.path.expanduser('~') + "/Downloads/" + Date + '.csv'
    Check_OutFile(resultpath)
    if os.path.isdir(Temproad):
        shutil.rmtree(Temproad)
    ProcessLog(evalue,".tgz",Check_Start,Check_End)

def open_Folder():
    os.system('open ~/Downloads')
                    
Root = Tk()
Root.title("计算时间")
win = Frame(Root, height=330, width=470)
win.grid_propagate(False)
win.grid()

lab = Label(win, text="文件路径:").grid(row=0, column=0,sticky = E)
lab1 = Label(win, text="生成路径:").grid(row=4, column=0,sticky = E)
lab2 = Label(win, text="开始参数:").grid(row=1, column=0,sticky = E)
lab6 = Label(win, text="结束参数:").grid(row=2, column=0,sticky = E)
lab7 = Label(win, text="~/Downloads").grid(row=4, column=1,sticky = W)
lab3 = Label(win, text="默认参数:").grid(row=6, column=0,sticky = E)
lab4 = Label(win, text="CM_Bundle_Verify/native_flash").grid(row=6, column=1,sticky = E)

e1 = Entry(win)
e1.grid(row=0, column=1)
e2 = Entry(win)
e2.grid(row=1, column=1)
e3 = Entry(win)
e3.grid(row=2, column=1)
b1 = Button(win, text="处理",command=btn_click)
b1.grid(row=0, column=3,sticky = E)
b1.configure(width=10, height=2)
b2 = Button(win, text="打开",command=open_Folder)
b2.grid(row=4, column=3,sticky = E)
b2.configure(width=5, height=2)

lb = Listbox(win,selectmode = MULTIPLE)
lb.grid(row=6, column=3,sticky = W)
for i in ['Memory','Battery']:
    lb.insert(END,str(i))

Root.mainloop()