#!/usr/bin/env python
# coding: UTF-8

import wx
import os, sys
import time, random
import commands
import re
import urllib
import urllib2
import shutil
import threading
import Queue

pass_file = os.path.dirname(sys.argv[0]) + '/passwd.txt'

q = Queue.Queue(0)
NUM_WORKERS = 10
mylock = threading.Lock()


class Frame(wx.Frame):
    def __init__(self):
        PDCAIPAdress = " "
        UserName = " "
        PassWord = " "
        try:
            with open(pass_file) as fd:
                for line in fd:
                    if "PDCAIP:" in line:
                        PDCAIPAdress = str(line).split('PDCAIP:')[1].replace('\n', '')
                    if "PDCAAccount:" in line:
                        UserName = str(line).split('PDCAAccount:')[1].replace('\n', '')
                    if "PDCAPassword:" in line:
                        PassWord = str(line).split('PDCAPassword:')[1].replace('\n', '')
        except:
            pass

        wx.Frame.__init__(self, None, -1, "pdcaCrawler", size=(450, 500), style=wx.DEFAULT_FRAME_STYLE)
        panel = wx.Panel(self, -1)
        basicLabel = wx.StaticText(panel, -1, "IP地址:", pos=(10, 20))
        pwdLabel = wx.StaticText(panel, -1, "用户:", pos=(10, 50))
        pwd1Label = wx.StaticText(panel, -1, "密码:", pos=(10, 80))
        pwd2Label = wx.StaticText(panel, -1, "SN List:", pos=(10, 110))
        pwd3Label = wx.StaticText(panel, -1, "关键字:", pos=(280, 110))

        self.basicText = wx.TextCtrl(panel, -1, PDCAIPAdress, size=(200, -1), pos=(70, 20))
        self.basic1Text = wx.TextCtrl(panel, -1, UserName, size=(200, -1), pos=(70, 50))
        self.basic4Text = wx.TextCtrl(panel, -1, "", size=(200, -1), pos=(70, 110))
        self.basic3Text = wx.TextCtrl(panel, -1, "", size=(80, -1), pos=(330, 110))
        self.pwdText = wx.TextCtrl(panel, -1, PassWord, size=(200, -1), pos=(70, 80), style=wx.TE_PASSWORD)
        self.basicText.SetInsertionPoint(0)

        self.button = wx.Button(panel, -1, "开始运行", size=(80, -1), pos=(330, 30))
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.button)
        self.button.SetDefault()

        # self.button1 = wx.Button(panel, -1, "停止运行", size=(80, -1), pos=(350, 60))
        # self.Bind(wx.EVT_BUTTON, self.OnClick1, self.button1)

        self.basic2Text = wx.TextCtrl(panel, -1, "", size=(400, 300), pos=(25, 150),
                                      style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH)
        self.basic2Text.SetInsertionPoint(0)

    def OnClick(self, event):
        self.basic2Text.Clear()
        IP = self.basicText.GetValue()

        self.writefile()

        logon_url = "http://%s/cgi-bin/WebObjects/QCR.woa/wa/logon" % IP
        self.displayinfo(logon_url)
        main()

    def writefile(self):
        list_file = self.basic4Text.GetValue()
        IP = self.basicText.GetValue()
        User = self.basic1Text.GetValue()
        PassWord = self.pwdText.GetValue()
        keyBits = self.basic3Text.GetValue()

        os.system('rm -rf %s' % pass_file)
        string = "PDCAIP:" + str(IP) + '\n' + "PDCAAccount:" + str(User) + '\n' + "PDCAPassword:" + str(PassWord) \
                 + '\n' + "keyBits:" + str(keyBits) + '\n' + "list_file:" + str(list_file)
        with open(pass_file, 'a') as d:
            d.write(string + '\n')

    def displayinfo(self, msg):
        self.basic2Text.AppendText(msg + '\n')
        # pass


class MyThread(threading.Thread):
    def __init__(self, input, worktype):
        self._jobq = input
        self._work_type = worktype
        threading.Thread.__init__(self)

    def run(self):
        while True:
            if self._jobq.qsize() > 0:
                self._process_job(self._jobq.get(), self._work_type)
            else:
                break

    def _process_job(self, job, worktype):
        doJob(job, worktype)


def crawl_sitemap(serial_number):
    '''
    Encode User passwd and url for crawl
    :param serial_number: for serial number crawl
    :return: no return
         job,IPaddress,Userer,Passwder,keyBitser
    '''
    postdata = urllib.urlencode({
        'UserName': UserName,
        'Password': PassWord
    })

    url_for_use = urllib2.Request(
        url=logon_url,
        data=postdata
    )

    for a in range(6):
        '''
           Set up x5 times for crawl, if all fail then exit.
           Crawl logon page.
        '''
        if a == 5:
            msg = "Logon QCR Fail."
            # frame.displayinfo(msg)
            os._exit(1)
        try:
            first_crawl = urllib2.urlopen(url_for_use, timeout=10).read()
        except:
            continue

        if re.search(r'<form name=".*?" method="post" action="(.*?)">', first_crawl):
            match = re.search(r'<a href="(.*?)">\s*?<span id = "product_history">Product History</span>', first_crawl)
            tmp_url = match.group(1)
            first_url = 'http://%s%s' % (PDCAIPAdress, tmp_url)
            break

    for b in range(6):
        '''
           Set up x5 times for crawl, if all fail then exit.
           Redirect to product history page.
        '''
        if b == 5:
            msg = "FAIL redirect to product history page."
            # frame.displayinfo(msg)
            os._exit(1)
        try:
            second_crawl = urllib2.urlopen(first_url, timeout=30).read()
        except:
            continue

        if re.search(r'<form name="f_7_1" method="post" action="(.*?)">(\s|.)*?<td>SN, PS, PO, or SO:</td>',
                     second_crawl):
            match = re.search(r'<form name="f_7_1" method="post" action="(.*?)">(\s|.)*?<td>SN, PS, PO, or SO:</td>',
                              second_crawl)
            tmp_url = match.group(1)
            second_url = 'http://%s%s' % (PDCAIPAdress, tmp_url)
            break

    postdata = urllib.urlencode({
        '7.1.1': serial_number,
        '7.1.3': 'Search',
        '7.1.7': '0',
    })

    url_for_use_two = urllib2.Request(
        url=second_url,
        data=postdata
    )

    for c in range(6):
        if c == 5:
            msg = "%s -> ERROR, FAIL to search find this SN on PDCA" % (serial_number)
            #frame.displayinfo(msg)
            os._exit(1)
        try:
            third_crawl = urllib2.urlopen(url_for_use_two, timeout=30).read()
        except:
            continue

        if re.findall(r'<a target="PARENT" href="(.*?)">View process logs</a>', third_crawl):
            tmp_url_three = re.findall(r'<a target="PARENT" href="(.*?)">View process logs</a>', third_crawl)[0]
            third_url = 'http://%s%s' % (PDCAIPAdress, tmp_url_three)
            break

    for d in range(6):
        if d == 5:
            msg = "%s -> ERROR, FAIL to search find this SN Log on PDCA" % (serial_number)
            # frame.displayinfo(msg)
            os._exit(1)
        try:
            fouth_crawl = urllib2.urlopen(third_url, timeout=30).read()
        except:
            continue

        if re.findall(r'<p><a href="(.*?)">Search all mounted process log servers</a></p>', fouth_crawl):
            tmp_url_four = \
                re.findall(r'<p><a href="(.*?)">Search all mounted process log servers</a></p>', fouth_crawl)[0]
            fourth_url = 'http://%s%s' % (PDCAIPAdress, tmp_url_four)
            break

    for e in range(6):
        if e == 5:
            msg = "%s -> ERROR, The last page Fail." % (serial_number)
            # frame.displayinfo(msg)
            os._exit(1)
        try:
            last_crawl = urllib2.urlopen(fourth_url, timeout=30).read()
        except:
            continue

        if re.search(r'<a href="(.*?)" name=".*?"><img', last_crawl):
            break
    sys.stdout.flush()
    #mylock.release()
    logs_url = re.findall(
        r'<tr>\s*?<td.*?>\s*?<font.*?>(.*?)</font>\s*?</td>\s*?<td.*?>\s*?<font.*?>.*?</font>\s*?</td>\s*?<td.*?>\s*?<font.*?>(.*?)</font>\s*?</td>\s*?<td.*?>\s*?<font.*?> <a href="(.*?)" name=".*?"><img',
        last_crawl)
    if len(logs_url) > 0:
        for i in logs_url:
            uul = 'http://%s%s?7,7' % (PDCAIPAdress, i[2])
            if formt in i[0] and "CQA" not in i[0]:  ## 剔除 CQA Log
                r = urllib2.urlopen(urllib2.Request(uul))
                with open(fpath + '/' + i[0], 'wb') as f:
                    shutil.copyfileobj(r, f)


def doJob(job, worktype):
    mylock.acquire()
    meg1 = "> Starting  - [" + str(job) + "]" + " - Thread@ " + str(worktype)
    wx.CallAfter(frame.displayinfo, meg1)
    crawl_sitemap(job)
    time.sleep(1)
    meg2 = "> Finished  - [" + str(job) + "]" + " - Thread@ " + str(worktype)
    #print threading.Thread.is_alive
    wx.CallAfter(frame.displayinfo, meg2)
    mylock.release()

def read_list(file):
    serial_number_list = []
    with open(file) as f_job:
        for line in f_job:
            sn = re.findall(r'C02[A-Z].{8}', line)
            if len(sn) > 0:
                serial_number_list.append(sn[0])

        return serial_number_list


def main():
    global fpath
    global logon_url
    global UserName
    global PassWord
    global formt
    global PDCAIPAdress

    try:
        with open(pass_file) as f:
            for line in f:
                if "PDCAIP:" in line:
                    PDCAIPAdress = str(line.split('PDCAIP:')[1]).replace('\n', '')
                if "PDCAAccount:" in line:
                    UserName = str(line.split('PDCAAccount:')[1]).replace('\n', '')
                if "PDCAPassword:" in line:
                    PassWord = str(line.split('PDCAPassword:')[1]).replace('\n', '')
                if "keyBits:" in line:
                    formt = str(line.split('keyBits:')[1]).replace('\n', '')
    except:
        meg = "用户信息不存在。"
        frame.displayinfo(meg)

    logon_url = "http://%s/cgi-bin/WebObjects/QCR.woa/wa/logon" % PDCAIPAdress

    try:
        with open(pass_file) as f:
            for line in f:
                if "list_file:" in line:
                    list_fileer = str(line.split('list_file:')[1]).replace('\n', '')
    except:
        meg = "用户信息不存在。"
        frame.displayinfo(meg)
        # os._exit(1)

    Date = time.strftime("%Y_%m_%d_%H_%M_%S")
    fpath = os.path.expanduser('~') + '/Downloads/' + Date

    os.system('mkdir -p %s' % fpath)

    sn_list = read_list(list_fileer)
    star = "Begin...."
    frame.displayinfo(star)

    for i in sn_list:
        q.put(i)
    print "Job Qsize:", q.qsize()
    for x in range(NUM_WORKERS):
        MyThread(q, x).start()


if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = Frame()
    frame.Show()
    app.MainLoop()
