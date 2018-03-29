#!/usr/bin/env python
# -*- coding: UTF-8 -*-

''' Hello, wxPython! program.'''

import wx

class Frame(wx.Frame):
    ''' Frame class that displays an image.'''
    def __init__(self,image,parent=None,id=-1,pos=wx.DefaultPosition,title='Hello,wxPython!'):
        '''Create a Frame instance and display image.'''
        temp = image.ConverToBitmap()
        size = temp.GetWidth(),temp.GetHeight()
        wx.Frame.__init__(self,parent,id,title,pos,size)
        self.bmp = wx.StaticBitmap(parent=self,bitmap=temp)


class App(wx.App):
    ''' Application class.'''
    def OnInit(self):

        image = wx.Image('wxPython.jpg',wx.BITMAP_TYPE_JPEG)
        self.frame = Frame(image)

        #frame = wx.Frame(parent=None,title='Bare')
        self.frame.Show()
        self.setTopWindow(self.frame)
        return True

def main():
    app = App()
    app.MainLoop()

if __name__ == '__main__':
    main()