#!/usr/bin/env python
# coding: UTF-8

import wx
import os, sys
import Queue
import threading
import time, random
import commands

q = Queue.Queue(0)
NUM_WORKERS = 1
mylock = threading.Lock()

class MyThread(threading.Thread):

    def __init__(self,input,worktype):
       self._jobq = input
       self._work_type = worktype
       threading.Thread.__init__(self)

    def run(self):
       while True:
           if self._jobq.qsize() > 0:
               self._process_job(self._jobq.get(),self._work_type)
           else:
               break

    def _process_job(self, job, worktype):
        doJob(job,worktype)

class Frame(wx.Frame):

    def __init__(self):
        global End

        wx.Frame.__init__(self,None,-1,"My App",size=(450,200))
        panel = wx.Panel(self,-1)
        basicLabel = wx.StaticText(panel, -1, "测试系统:", pos=(10, 20))
        self.basicText = wx.TextCtrl(panel, -1, "", size=(200, -1), pos=(80, 20))
        self.basic1Text = wx.TextCtrl(panel, -1, "", size=(200, -1), pos=(80, 50))
        self.basicText.SetInsertionPoint(0)
        pwdLabel = wx.StaticText(panel, -1, "出货系统:", pos=(10, 50))
        pwd1Label = wx.StaticText(panel, -1, "开机密码:", pos=(10, 80))
        pationLabel = wx.StaticText(panel, -1, "下载分区:", pos=(10, 110))
        self.pwdText = wx.TextCtrl(panel, -1, "", size=(80, -1), pos=(80, 80), style=wx.TE_PASSWORD)
        self.pation1 = wx.TextCtrl(panel, -1, "70", size=(30, -1), pos=(80, 110))
        self.pation2 = wx.TextCtrl(panel, -1, "1", size=(30, -1), pos=(120, 110))
        self.pation3 = wx.TextCtrl(panel, -1, "80", size=(30, -1), pos=(160, 110))
        self.button = wx.Button(panel, -1, "开始", size=(80, -1), pos=(350, 30))
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.button)
        self.button.SetDefault()

    def OnClick(self,event):
        TestBundle_ = self.basicText.GetValue()
        TestBundle = find_file(FindPath,str(TestBundle_))
        CMbundle_ = self.basic1Text.GetValue()
        CMbundle = find_file(FindPath, str(CMbundle_))
        Password = self.pwdText.GetValue()
        Partiton1 = self.pation1.GetValue()
        Partiton2 = self.pation2.GetValue()
        Partiton3 = self.pation3.GetValue()

        Stoping1 = False
        Stoping2 = False
        Stoping = False
        Status = False
        if not TestBundle_ or ".dmg" not in TestBundle:
            dlg1 = wx.MessageDialog(None, "测试系统不存在! 请检查后..重新输入...,", '错误', wx.YES_NO | wx.ICON_QUESTION)
            result = dlg1.ShowModal()
            dlg1.Destroy()
            Stoping1 = True
        if not CMbundle_ or ".dmg" not in CMbundle:
            dlg2 = wx.MessageDialog(None, "出货系统未输入或者不存在! 是否继续？...,", '错误', wx.YES_NO | wx.ICON_QUESTION)
            if dlg2.ShowModal() == wx.ID_OK:
                Stoping2 = False
            else:
                Stoping2 = True
                CMbundle = "None"
        if Stoping1 == True and Stoping2 == True:
            Stoping = True
        if not Password and not Stoping:
            dlg = wx.MessageDialog(None, '未输入开机密码，是否继续...','错误', wx.YES_NO | wx.ICON_QUESTION)
            if dlg.ShowModal() == wx.ID_NO:
                Stoping = True
            dlg.Destroy()
        if not Stoping:
            dlg = wx.SingleChoiceDialog(None,'请选择外接磁盘名字?', '磁盘选择',['disk1', 'disk2', 'disk3', 'disk4', 'disk5'])
            if dlg.ShowModal() == wx.ID_OK:
                response = dlg.GetStringSelection()
                Status = True
            else:
                response = "None"
                Status = False
        if Status:
            result1 = "TestBundle:" + TestBundle + '\n' + "CMBundle:" + CMbundle + '\n'
            result2 = "Password:" + Password + '\n' + "TestPardition1:" + Partiton1 + '\n'
            result3 = "TestPardition2:" + Partiton2 + '\n' + "TestPardition3:" + Partiton3 + '\n' + "DISK:" + response
            endresult = result1 + result2 + result3
            writefile(endresult,Pathroad)
            print "begin...."
            a = 1
            for i in xrange(a):
                q.put(i)
            print "job qsize:",q.qsize()
            #mylock.acquire()
            for x in range(NUM_WORKERS):
                MyThread(q,x).start()
                self.button.SetLabel("运行")
                #q.join()
            #mylock.release()

def doJob(job, worktype):
    os.system('open -a /Applications/*/Terminal.app %s'%cmd)

def writefile(string,file):
    try:
        with open(file, 'w') as d:
            d.write(string + '\n')
    except IOError as i:
        print ('IOError:',i)

def find_file(path,formet):
    try:
        fns = [os.path.join(root, fn) for root, dirs, files in os.walk(path) for fn in files]
        for f in fns:
            if os.path.isfile(f):
                if formet in f:
                    return f
    except IOError as o:
        print ('IOError',o)

if __name__ == '__main__':
    FindPath = os.path.expanduser('~') + '/Desktop'
    Pathroad = os.path.dirname(sys.argv[0]) + '/result.txt'
    cmd = os.path.dirname(sys.argv[0]) + '/App_Command.sh'
    app = wx.PySimpleApp()
    frame = Frame()
    frame.Show()
    app.MainLoop()