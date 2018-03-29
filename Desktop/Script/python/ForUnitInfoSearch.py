#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import sys
from Tkinter import *

class UnitsInfo(object):
    def __init__(self,pathroad,parameter):
        self.path = pathroad
        self.pater = parameter

    def SearchFile(self):
        with open(self.path) as fi:
            for line in fi:
                if self.pater in line:
                    self.SerialNumber = line.split()[5].split('+')[0]
                    self.ModelTable = line.split()[5].split('+')[1]
                    self.UnitNumber = line.split()[4]
                    self.Config = line.split()[3]
                    self.Build = line.split()[2]
                    self.InputDate = line.split()[1]
    def show(self):
        root = Tk()
        root.title("信息查询")
        win = Frame(root, height=150, width=500)
        win.grid_propagate(False)
        win.grid()

        Text = Entry(win)
        Text.columnconfigure(2)
        Text.grid(row=0, column=1)
        button = Button(win, text="查询", command=running).grid(row=0, column=2)

        Label1 = Message(win, text=self.UnitNumber).grid(row=1, column=1)
        Label2 = Message(win, text=self.SerialNumber).grid(row=2, column=1)
        Label3 = Message(win, text=self.ModelTable).grid(row=3, column=1)
        Label4 = Message(win, text=self.Config).grid(row=3, column=2)
        Label5 = Message(win, text=self.InputDate).grid(row=4, column=1)

        root.mainloop()



def running():
    pathroad = os.path.dirname(sys.argv[0]) + "/Unitsinfo.txt"
    parameter = Text.get()
    UnitsInfo(pathroad,parameter)

if __name__ == '__main__':
    root = Tk()
    root.title("信息查询")
    win = Frame(root, height=150, width=500)
    win.grid_propagate(False)
    win.grid()

    Text = Entry(win)
    Text.columnconfigure(2)
    Text.grid(row=0, column=1)
    button = Button(win, text="查询", command=running).grid(row=0,column=2)

    root.mainloop()




