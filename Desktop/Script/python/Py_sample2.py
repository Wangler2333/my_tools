#!/usr/bin/env python
# coding: UTF-8

import wx

class InsertFrame(wx.Frame):
    def __init__(self,parent,id):
        wx.Frame.__init__(self,parent,id,'Frame With Button',size=(500,300))
        panel = wx.Panel(self)
        button = wx.Button(panel,label="退出",pos=(180,10),size=(80,50))
        button1 = wx.Button(panel, label="退出", pos=(200, 50), size=(80, 50))
        self.Bind(wx.EVT_BUTTON,self.OnCloseMe,button)
        self.Bind(wx.EVT_CLOSE,self.OnCloseWindow)

    def OnCloseMe(self,event):
        self.Close(True)

    def OnCloseWindow(self,event):
        self.Destroy()

if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = InsertFrame(parent=None,id=-1)
    frame.Show()
    app.MainLoop()