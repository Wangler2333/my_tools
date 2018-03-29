#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from Tkinter import *

top = Tk()

def resize(ev=None):
    label.config(font='Helvetica -%d bold' % scale.get())

top.geometry('450x300')

label = Label(top, text='Hello World!',
              font='Helvetica -12 bold')
label.pack(fill=Y, expand=1)

scale = Scale(top, from_=10, to=100,
              orient=HORIZONTAL, command=resize)
scale.set(22)
scale.pack(fill=X,expand=1)

quit = Button(top, text='QUIT',
              command=top.quit, activeforeground='white',
              activebackground='red')
quit.pack()

mainloop()