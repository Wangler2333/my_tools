#!/usr/bin/python
# -*- coding: UTF-8 -*-
# Create by Saseny on 2017/03/16
'''
导出PTF内所有测试项，生成SCV文件，文件生成路径 ~/Downloads.
'''

import json
import time
import os
from Tkinter import *
import ttk

def writefile(string,file):
    try:
        with open(file, 'a') as d:
            d.write(string + '\n')
    except IOError as i:
        print ('IOError_4:',i)

def Check_OutFile(file):
    try:
        if not os.path.isfile(file):
            title = "Test Item, Error Code, Test Info, Message"
            writefile(title,file)
    except TypeError as h:
        print ('TypeError_1:',h)

def Process_Start(filename):
    Date = time.strftime("%Y_%m_%d_%H_%M_%S")
    filepath = os.path.expanduser('~') + "/Downloads/" + Date + '.csv'
    with open(filename) as obj:
        numbers = json.load(obj)
    dd = len(numbers[u'data'][u'tests'])
    ac = []
    dicts = {}
    dicts = numbers[u'data']
    no = 0
    Check_OutFile(filepath)
    while no < dd:
        try:
            a = numbers[u'data'][u'tests'][no][u'category']
            b = numbers[u'data'][u'tests'][no][u'key']
            d = numbers[u'data'][u'tests'][no][u'name']
            e = numbers[u'data'][u'tests'][no][u'description']
            c = str(a) + "," + str(b) + "," + str(d.replace(',', '')) + "," + str(e.replace(',', ''))
            writefile(c,filepath)
            no += 1
        except IndexError as e:
            print ('IndexError:',e)

def btn_click():
    evalue = e.get()
    Process_Start(evalue)

def open_Folder():
    os.system('open ~/Downloads')

Root = Tk()
Root.title("PTF导出CSV文件")
#Root.geometry('340x75')
win = Frame(Root, height=80, width=340)
win.grid_propagate(False)
win.grid()

lab = Label(win,text = "文件路径:").grid(row = 0, column = 1, sticky = W)
lab1 = Label(win,text = "结果生成路径: ~/Downloads").grid(row = 1, column = 2, sticky = E+W)

e = Entry(win)
e.grid(row = 0, column = 2, sticky = E)

b1 = Button(win, text = "处理" , command = btn_click)
b1.grid(row = 0, column = 3)
b1.configure(width = 5, height = 2)

b2 = Button(win, text = "打开" , command = open_Folder)
b2.grid(row = 1, column = 3)
b2.configure(width = 5, height = 2)

Root.mainloop()