#!/usr/bin/env python
# coding: UTF-8

import wx
import os, sys
import threading
import time, random

def writefile(string,file):
    try:
        with open(file, 'w') as d:
            d.write(string + '\n')
    except IOError as i:
        print ('IOError:',i)

#def download():
    #print "1233445"
    #os.system('/Applications/Download.app/Contents/Resources/App_Command.sh')

class WorkerThread(threading.Thread):
    '''
    This just simulates some long-running task that periodically sends a message to the GUI thread.
    '''

    def __init__(self, threadNum, window):
        threading.Thread.__init__(self)
        self.threadNum = threadNum
        self.window = window
        self.timeToQuit = threading.Event()
        self.timeToQuit.clear()
        self.messageCount = random.randint(10, 20)
        self.messageDelay = 0.1 + 2.0 * random.random()

    def stop(self):
        self.timeToQuit.set()

    def run(self):
        msg = "Thread %d iterating %d times with a delay of %1.4f\n" % (
        self.threadNum, self.messageCount, self.messageDelay)
        wx.CallAfter(self.window.LogMessage, msg)
        for i in range(1, self.messageCount + 1):
            self.timeToQuit.wait(self.messageDelay)
            if self.timeToQuit.isSet():
                break
            msg = "Message %d from thread %d\n" % (i, self.threadNum)
            wx.CallAfter(self.window.LogMessage, msg)
        else:
            wx.CallAfter(self.window.ThreadFinished, self)

class Frame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self,None,-1,"My App",size=(600,380),style=wx.CLOSE_BOX | wx.MAXIMIZE_BOX | wx.MINIMIZE_BOX)
        panel = wx.Panel(self,-1)
        self.count = 0

        self.FileDialog1 = wx.FileDialog(panel, message="选择测试系统", defaultDir="", defaultFile="", wildcard="*.dmg",
                                   style=0,)
        if self.FileDialog1.ShowModal() == wx.ID_OK:
            self.filename1 = self.FileDialog1.GetPath()

        self.FileDialog2 = wx.FileDialog(panel, message="选择出货系统,可不选，不选则不下载", defaultDir="", defaultFile="", wildcard="*.dmg",
                                        style=0,pos=wx.DefaultPosition )
        if self.FileDialog2.ShowModal() == wx.ID_OK:
            self.filename2 = self.FileDialog2.GetPath()
        else:
            self.filename2 = ""

        self.FileDialog1.Destroy()
        self.FileDialog2.Destroy()

        basicLabel = wx.StaticText(panel, -1, "测试系统:", pos=(10, 20))

        name1 = str(self.filename1.split('/')[-1])
        name2 = str(self.filename2.split('/')[-1])

        basicText1 = wx.TextCtrl(panel, -1, name1, pos=(80, 20),size=(175,-1))
        basicText2 = wx.TextCtrl(panel, -1, name2, pos=(80, 50),size=(175,-1))

        pwdLabel = wx.StaticText(panel, -1, "出货系统:", pos=(10, 50))
        pwd1Label = wx.StaticText(panel, -1, "开机密码:", pos=(10, 80))
        pationLabel = wx.StaticText(panel, -1, "下载分区:", pos=(10, 110))
        #self.basic1Text = wx.TextCtrl(panel, -1, "", size=(200, -1), pos=(80, 50))

        self.pwdText = wx.TextCtrl(panel, -1, "", size=(80, -1), pos=(80, 80), style=wx.TE_PASSWORD)

        self.pation1 = wx.TextCtrl(panel, -1, "70", size=(30, -1), pos=(80, 110))
        self.pation2 = wx.TextCtrl(panel, -1, "1", size=(30, -1), pos=(120, 110))
        self.pation3 = wx.TextCtrl(panel, -1, "80", size=(30, -1), pos=(160, 110))

        self.log = wx.TextCtrl(panel, -1, "", style=wx.TE_RICH | wx.TE_MULTILINE, pos=(40,170),size=(520,150))

        self.button = wx.Button(panel, -1, "开始", size=(80, -1), pos=(350, 30))
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.button)
        self.button.SetDefault()

    def OnClick(self,event):
        TestBundle = self.filename1
        CMbundle = self.filename2
        Password = self.pwdText.GetValue()
        Partiton1 = self.pation1.GetValue()
        Partiton2 = self.pation2.GetValue()
        Partiton3 = self.pation3.GetValue()

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
        thread = WorkerThread(self.count, self)
        thread.start()
        #writefile(RESULT,Pathroad)
        #if Status == True:
            #download()

if __name__ == '__main__':
    Pathroad = os.path.dirname(sys.argv[0]) + '/result.txt'
    app = wx.PySimpleApp()
    frame = Frame()
    frame.Show()
    app.MainLoop()
