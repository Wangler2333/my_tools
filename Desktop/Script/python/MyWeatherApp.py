#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import wx

class Frame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, "pdcaCrawler", size=(1300, 1000), style=wx.DEFAULT_FRAME_STYLE)
        panel = wx.Panel(self, -1)

if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = Frame()
    frame.Show()
    app.MainLoop()
