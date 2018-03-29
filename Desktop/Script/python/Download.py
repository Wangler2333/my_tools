#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
from Tkinter import *

def writefile(string,file):
    try:
        with open(file, 'w') as d:
            d.write(string + '\n')
    except IOError as i:
        print ('IOError:',i)

def DiskList():
    os.system('open -a /Applications/*/Terminal.app /usr/local/bin/diskutillist.sh')

def Quit():
    os.system('killall -m Terminal')

def Start():
    FilePath = os.path.expanduser('~') + "/Downloads/Default.txt"
    TestBundel = "TestBundle:" + entry1.get()
    CMBundle = "CMBundle:" + entry2.get()
    TestSize = "TestSize:" + entry3.get()
    DiagSize = "DiagSize:" + entry4.get()
    RecoverySize = "RecoverySize:" + entry5.get()
    Disk = "None"
    if lb.selection_includes(0) == True:
        Disk = "DISK:disk1"
    if lb.selection_includes(1) == True:
        Disk = "DISK:disk2"
    if lb.selection_includes(2) == True:
        Disk = "DISK:disk3"
    if lb.selection_includes(3) == True:
        Disk = "DISK:disk4"
    if lb.selection_includes(4) == True:
        Disk = "DISK:disk5"

    String = TestBundel + '\n' + CMBundle  + '\n' + TestSize + '\n' + DiagSize + '\n' + RecoverySize + '\n' + Disk
    writefile(String,FilePath)
    os.system('open -a /Applications/*/Terminal.app /usr/local/bin/AppDownloadFile.sh')


Download = Tk()
Download.title("Doanload")
root = Frame(Download, height=220, width=480)
root.grid_propagate(False)
root.grid()

Label1 = Label(root,text="测试系统:").grid(row=1,column=0,sticky = W)
Label2 = Label(root,text="出货系统:").grid(row=2,column=0,sticky = W)
Label3 = Label(root,text="Testsize:").grid(row=3,column=0,sticky = W)
Label4 = Label(root,text="Diags:").grid(row=4,column=0,sticky = W)
Label5 = Label(root,text="Recovery:").grid(row=5,column=0,sticky = W)

e = StringVar()
entry1 = Entry(root,textvariable = e)
entry1.grid(row=1, column=2)
e.set('J79A_PVT_3-1_0.0B1.dmg')

f = StringVar()
entry2 = Entry(root,textvariable = f)
entry2.grid(row=2, column=2)
f.set('694-07371-039.dmg')

g = StringVar()
entry3 = Entry(root,textvariable = g)
entry3.grid(row=3, column=2)
g.set('70g')

h = StringVar()
entry4 = Entry(root,textvariable = h)
entry4.grid(row=4, column=2)
h.set('1g')

i = StringVar()
entry5 = Entry(root,textvariable = i)
entry5.grid(row=5, column=2)
i.set('80g')

lb = Listbox(root)
lb.grid(row=1, rowspan=5, column=3,sticky = W)
for i in ['Disk1','Disk2','Disk3','Disk4','Disk5']:
    lb.insert(END,str(i))
lb.selection_set(0)

Button1 = Button(root, text="开始",command=Start)
Button1.grid(row=6, column=3,sticky = E)
Button1.configure(width=8, height=2)

Button2 = Button(root, text="查看 Disk", command = DiskList)
Button2.grid(row=6, column=2,sticky = E)
Button2.configure(width=8, height=2)

Button2 = Button(root, text="退出", command = Quit)
Button2.grid(row=6, column=0,sticky = E)
Button2.configure(width=5, height=2)

root.mainloop()