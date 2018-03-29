#!/usr/bin/env python

from Tkinter import *


master = Tk()
Label(master, text="First").grid(row=0)
Label(master, text="Second").grid(row=1)

e1 = Entry(master)
e2 = Entry(master)

e1.grid(row=0, column=1)
e2.grid(row=1, column=1)

mainloop()

#def Submit():
#    s1 = ent1.get()
#    s2 = ent2.get()
#    if s1 == "freedom" and s2 == "123":
#        lab3["text"] = "Confrim"
#    else:
#        lab3["text"] = "Error!"
#    ent1.delete(0,len(s1))
#    ent2.delete(0,len(s2))


#root = Tk()

#lab1 = Label(root,text = "User:")
##lab1.grid(row = 0,column = 0,sticky = W)
#lab1.pack()

#ent1 = Entry(root)
#ent1.grid(row = 0,column = 1,sticky = W)
#ent1.pack()

#lab2 = Label(root,show = "Password:")
#lab2.grid(row = 1,column = 0)
#lab2.pack()

#ent2 = Entry(root,show = "*")
#ent2.grid(row = 1,column = 1,sticky = W)
#ent2.pack()

#button = Button(root,text = "Submit",command = Submit)
#button.grid(row = 2,column = 1,sticky = E)
#button.pack()

#lab3 = Label(root,text = "")
#lab3.grid(row = 3,column = 1,sticky = W)
#lab3.pack()

#button2 = Button(root,text = "Quit", command = quit)
#button2.grid(row = 3,column = 1,sticky = E)
#button2.pack()
#root.title("Register")
#root.mainloop()
