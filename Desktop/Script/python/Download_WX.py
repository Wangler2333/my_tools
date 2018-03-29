#!/usr/bin/env python
# coding: UTF-8

import wx
import os, sys
import Queue
import threading
import time, random
import commands

def writefile(string,file):
    try:
        with open(file, 'w') as d:
            d.write(string + '\n')
    except IOError as i:
        print ('IOError:',i)

def download():
    #print "1233445"
    os.system('/Applications/Download.app/Contents/Resources/App_Command.sh')

class Frame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self,None,-1,"My App",size=(450,180))
        panel = wx.Panel(self,-1)

        self.FileDialog1 = wx.FileDialog(panel, message="选择测试系统", defaultDir="", defaultFile="", wildcard="*.dmg",
                                   style=0,)
        if self.FileDialog1.ShowModal() == wx.ID_OK:
            self.filename1 = self.FileDialog1.GetPath()
            #self.ReadFile()
        #self.SetTitle(self.title + ' -- ' + self.filename)

        self.FileDialog2 = wx.FileDialog(panel, message="选择出货系统,可不选，不选则不下载", defaultDir="", defaultFile="", wildcard="*.dmg",
                                        style=0, )
        if self.FileDialog2.ShowModal() == wx.ID_OK:
            self.filename2 = self.FileDialog2.GetPath()
        else:
            self.filename2 = ""

        self.FileDialog1.Destroy()
        self.FileDialog2.Destroy()

        basicLabel = wx.StaticText(panel, -1, "测试系统:", pos=(10, 20))
        #self.basicText = wx.TextCtrl(panel, -1, "", size=(200, -1), pos=(80, 20))
        #self.basicText.SetInsertionPoint(0)

        name1 = str(self.filename1.split('/')[-1])
        name2 = str(self.filename2.split('/')[-1])

        Basiclabel1 = wx.StaticText(panel, -1, name1, pos=(80, 20))
        Basiclabel2 = wx.StaticText(panel, -1, name2, pos=(80, 50))

        pwdLabel = wx.StaticText(panel, -1, "出货系统:", pos=(10, 50))
        pwd1Label = wx.StaticText(panel, -1, "开机密码:", pos=(10, 80))
        pationLabel = wx.StaticText(panel, -1, "下载分区:", pos=(10, 110))
        #self.basic1Text = wx.TextCtrl(panel, -1, "", size=(200, -1), pos=(80, 50))

        self.pwdText = wx.TextCtrl(panel, -1, "", size=(80, -1), pos=(80, 80), style=wx.TE_PASSWORD)

        self.pation1 = wx.TextCtrl(panel, -1, "70", size=(30, -1), pos=(80, 110))
        self.pation2 = wx.TextCtrl(panel, -1, "1", size=(30, -1), pos=(120, 110))
        self.pation3 = wx.TextCtrl(panel, -1, "80", size=(30, -1), pos=(160, 110))

        #slider = wx.Slider(panel, 100, 25, 1, 100, pos=(10, 100),size=(250, -1),style=wx.SL_HORIZONTAL | wx.SL_AUTOTICKS | wx.SL_LABELS)
        #slider.SetTickFreq(5,1)

        self.button = wx.Button(panel, -1, "开始", size=(80, -1), pos=(350, 30))
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.button)
        self.button.SetDefault()

    #    self.count = 0
    #    self.gauge = wx.Gauge(panel, -1, 500, (20, 200), (450, 25))
    #    self.gauge.SetBezelFace(3)
    #    self.gauge.SetShadowWidth(3)
    #    self.Bind(wx.EVT_IDLE, self.OnIdle)

    #def OnIdle(self, event):
    #    self.count = self.count + 1
        #if self.count >= 50:
            #self.count = 0
    #    self.gauge.SetValue(self.count)

    def OnClick(self,event):
        TestBundle = self.filename1
        CMbundle = self.filename2
        Password = self.pwdText.GetValue()
        Partiton1 = self.pation1.GetValue()
        Partiton2 = self.pation2.GetValue()
        Partiton3 = self.pation3.GetValue()

        dlg1 = wx.MessageDialog(None, '测试系统不存在! 请重新输入...', '错误', wx.YES_NO | wx.ICON_QUESTION)
        result = dlg1.ShowModal()
        dlg1.Destroy()

        dlg2 = wx.MessageDialog(None, '出货系统不存在! 请重新输入...', '错误', wx.YES_NO | wx.ICON_QUESTION)
        result = dlg2.ShowModal()
        dlg2.Destroy()

        dlg = wx.SingleChoiceDialog(None,'请选择外接磁盘名字?', '磁盘选择',['disk1', 'disk2', 'disk3', 'disk4', 'disk5'])

        if dlg.ShowModal() == wx.ID_OK:
            response = dlg.GetStringSelection()
            Status = True
        else:
            response = None
            Status = False

        self.button.SetLabel("运行")
        REsult1 = "TestBundle:" + TestBundle + '\n' + "CMBundle:" + CMbundle + '\n'
        REsult2 = "Partiton1:" + Partiton1 + '\n' + "Partiton2:" + Partiton2 + '\n' + "Partiton3:" + Partiton3 + '\n'
        REsult3 = "Disk:" + str(response) + '\n' + "Password:" + Password

        RESULT = REsult1 + REsult2 + REsult3
        writefile(RESULT,Pathroad)
        if Status == True:
            download()

        #print TestBundle,CMbundle,Password,Partiton1,Partiton2,Partiton3,str(response),Status

if __name__ == '__main__':
    Pathroad = os.path.dirname(sys.argv[0]) + '/result.txt'
    app = wx.PySimpleApp()
    frame = Frame()
    frame.Show()
    app.MainLoop()
