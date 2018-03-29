#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import wx

class PySimpleApp(wx.App):
    def __init__(self,redirect=False,filename=None,useBestVisual=False,clearSigInt=True):
        wx.App.__init__(self,redirect,filename,useBestVisual,clearSigInt)

    def OnInit(self):
        return True

if __name__ =='__main__':
    app = wx.PySimpleApp()
    frame = MyNewFrame(None)
    frame.Show(True)
    app.MainLoop()