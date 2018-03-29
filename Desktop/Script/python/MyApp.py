#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# __author__: Saseny Zhou
# Created on 2017/08/01 witsh the first version


import wx
import os
import sys
import time
import threading
import thread
import csv
import urllib2
import re
import commands
import pexpect
import mysql.connector
import BeautifulSoup
import lxml
import random
import Queue
import urllib
import shutil
import collections
import glob
import requests
import wx.lib.buttons as buttons
import plistlib

q = Queue.Queue(0)
NUM_WORKERS = 1
mylock = threading.Lock()

# dir_path = os.path.dirname(sys.argv[0])
dir_path = '/Users/Shared'
pdca_file = dir_path + '/file/pdca_info.txt'
display_log = dir_path + '/file/log.log'
command_de_en_code = os.path.dirname(sys.argv[0]) + '/tools'

global frame


class Frame(wx.Frame):
    def __init__(self):
        # ------------------------------------------------------------------------------------------------------------ #
        # PDCA 信息提前读取
        PDCAIPAdress = "PDCA IP Address"
        UserName = "PDCA Account"
        PassWord = "PDCA Password"
        try:
            with open(pdca_file) as fd:
                for line in fd:
                    if "PDCAIP:" in line:
                        PDCAIPAdress = str(line).split('PDCAIP:')[1].replace('\n', '')
                    if "PDCAAccount:" in line:
                        UserName = str(line).split('PDCAAccount:')[1].replace('\n', '')
                    if "PDCAPassword:" in line:
                        PassWord = str(line).split('PDCAPassword:')[1].replace('\n', '')
        except:
            pass
        # ------------------------------------------------------------------------------------------------------------ #
        wx.Frame.__init__(self, None, -1, "MyApp", size=(1000, 800), style=wx.DEFAULT_FRAME_STYLE)
        panel = wx.Panel(self, -1)

        font = wx.Font(100, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False, 'Courier New')
        self.SetFont(font)

        self.button = buttons.GenButton(panel, -1, 'Start', size=(180, 90), pos=(780, 30))
        self.button.SetFont(wx.Font(20, wx.SWISS, wx.NORMAL, wx.BOLD, False))
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.button)
        self.button.SetDefault()
        self.button.SetBezelWidth(5)
        self.button.SetBackgroundColour('Green')

        self.basicText1 = wx.TextCtrl(panel, -1, "Enter File Path Road or Others", size=(700, 25), pos=(50, 80),
                                      style=wx.TE_LEFT)

        self.basic2Text = wx.TextCtrl(panel, -1, "", size=(900, 450), pos=(50, 300),
                                      style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH)
        self.basic2Text.SetInsertionPoint(0)

        Label6 = wx.StaticText(panel, -1, "剩余:", pos=(50, 280))
        self.text_eight = wx.TextCtrl(panel, -1, "", size=(45, 20), pos=(83, 280), style=wx.TE_LEFT | wx.TE_READONLY)
        # ------------------------------------------------------------------------------------------------------------ #
        #  时间更新
        self.basic3Text = wx.TextCtrl(panel, -1, "", size=(155, 20), pos=(50, 30),
                                      style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_CENTER)
        self.basic3Text.SetInsertionPoint(0)
        # ------------------------------------------------------------------------------------------------------------ #
        #  天气更新
        self.basic4Text = wx.TextCtrl(panel, -1, "", size=(520, 38), pos=(230, 20),
                                      style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_LEFT)
        self.basic4Text.SetInsertionPoint(0)
        # ------------------------------------------------------------------------------------------------------------ #
        Label1 = wx.StaticText(panel, -1, "PDCA 信息:", pos=(750, 150))
        self.Text1 = wx.TextCtrl(panel, -1, PDCAIPAdress, size=(200, 20), pos=(750, 180))
        self.Text2 = wx.TextCtrl(panel, -1, UserName, size=(200, 20), pos=(750, 210))
        self.Text3 = wx.TextCtrl(panel, -1, PassWord, size=(200, 20), pos=(750, 240), style=wx.TE_PASSWORD)
        self.Text4 = wx.TextCtrl(panel, -1, "Log Keys", size=(100, 20), pos=(850, 150), style=wx.TE_CENTER)
        # ------------------------------------------------------------------------------------------------------------ #
        #  CM 输入框
        self.basic5Text = wx.TextCtrl(panel, -1, "CM Bundle Name", size=(200, 20), pos=(750, 270),
                                      style=wx.TE_MULTILINE | wx.TE_LEFT)
        self.basic5Text.SetInsertionPoint(0)
        # ------------------------------------------------------------------------------------------------------------ #

        self.sampleList = ['空选项(默认)', 'PDCA Log 下载', 'Download Log 处理', '79A Runin 时间计算', 'Bundle Download',
                           '等待更新', '等待更新', '等待更新', '等待更新', '文件解密', '文件加密',
                           '天气播报', '检查磁盘信息', '解释说明', '未来7天天气', '清除记录']
        self.checkbox = wx.RadioBox(panel, -1, '功能选择栏(单选)', (50, 120), wx.DefaultSize, self.sampleList, 4,
                                    wx.RA_SPECIFY_COLS)
        # ------------------------------------------------------------------------------------------------------------ #
        # 进度条显示
        self.count = 0
        self.gauge = wx.Gauge(panel, -1, 50, (50, 250), (650, 25))
        self.gauge.SetBezelFace(5)
        self.gauge.SetShadowWidth(5)
        self.Bind(wx.EVT_IDLE, self.OnIdle)
        self.text_eight.SetBackgroundColour('Green')
        # ------------------------------------------------------------------------------------------------------------ #
        # 网络状态显示
        self.img1 = wx.Image(os.path.dirname(sys.argv[0]) + '/png/' + 'pass.png',
                             wx.BITMAP_TYPE_PNG).ConvertToBitmap()  # pass
        self.img2 = wx.Image(os.path.dirname(sys.argv[0]) + '/png/' + 'fail.png',
                             wx.BITMAP_TYPE_PNG).ConvertToBitmap()  # fail

        Label2 = wx.StaticText(panel, -1, "PDCA", pos=(685, 180))
        self.network_one = wx.BitmapButton(panel, -1, self.img2, size=(30, 30), pos=(690, 200))
        Label3 = wx.StaticText(panel, -1, "SINA", pos=(685, 130))
        self.network_two = wx.BitmapButton(panel, -1, self.img2, size=(30, 30), pos=(690, 150))

        try:
            App_version = plistlib.readPlist(os.path.dirname(sys.argv[0]).replace('Resources', '') + 'Info.plist')[
                'CFBundleVersion']
        except:
            App_version = ""
        Label4 = wx.StaticText(panel, -1, App_version, pos=(945, 753))

        Label5 = wx.StaticText(panel, -1, "Log行数:", pos=(170, 280))
        self.text_nine = wx.TextCtrl(panel, -1, "", size=(55, 20), pos=(230, 280),
                                     style=wx.TE_LEFT | wx.TE_READONLY)
        self.text_nine.SetBackgroundColour('Green')

        time_start_add()  # 打开时间线程显示当前时间并实时刷新，以及显示天气情况
        weather_start()  # 打开天气更新线程，需连接网络状态
        thread.start_new(net_work_check, ())  # 检查网络状态
        thread.start_new(read_log, ())  # 显示历史记录
        thread.start_new(check_log_row, ())  # 检查log存储行数，大于1000时显示红色

    def OnClick(self, event):
        # 检查时间显示和天气显示是否为空
        if self.basic3Text.GetValue() == "" or self.basic4Text.GetValue() == "":
            time_start_add()
            weather_start()
            thread.start_new(net_work_check, ())
            self.basic2TextDisplay("时间和天气刷新")

        self.writefiley()
        file_path = self.basicText1.GetValue().encode('utf-8')
        choose = self.checkbox.GetStringSelection().encode('utf-8')
        read_info()

        self.basic2TextDisplay("File Path: \t" + file_path)
        self.basic2TextDisplay("Function Choose: \t" + choose)

        if choose == str(self.sampleList[1]):
            thread.start_new(download_log, ())
        if choose == str(self.sampleList[2]):
            thread.start_new(for_download_log_check, ())
        if choose == str(self.sampleList[3]):
            thread.start_new(for_runin_time_check, ())
        if choose == str(self.sampleList[4]):
            pass
            # thread.start_new(for_runin_time_check, ())
        if choose == str(self.sampleList[-1]):
            self.basic2Text.Clear()
            os.system('rm -rf %s' % display_log)
        if choose == str(self.sampleList[-2]):
            self.futureWeather()
        if choose == str(self.sampleList[-3]):
            thread.start_new(Explain, ())
        if choose == str(self.sampleList[-4]):
            thread.start_new(check_extend_disk, ())
        if choose == str(self.sampleList[-5]):
            thread.start_new(speak_weather, ())
        if choose == str(self.sampleList[-6]):
            thread.start_new(encode_file, ())
        if choose == str(self.sampleList[-7]):
            thread.start_new(decode_file, ())

            # self.OnIdle(event)

    def show_start_or_fail(self, a):
        '''
        :param a:      给定需要的状态值，1代表绿色，0代表红色
        :return:       更改开始按钮显示的颜色
        '''
        if a == 1:
            self.button.SetBackgroundColour('Red')
            self.button.SetLabel('Running')
            self.button.Enable(False)
        elif a == 0:
            self.button.SetBackgroundColour('Green')
            self.button.SetLabel('Start')
            self.button.Enable(True)

    def check_log(self, number):
        self.text_nine.SetLabel(str(number))
        if int(number) >= 1000:
            self.text_nine.SetBackgroundColour('Red')

    def futureWeather(self):
        thread.start_new(futher_weather, ())

    def basic2TextDisplay(self, msg, writer=None):
        current_time = time.strftime("%Y/%m/%d %H:%M:%S")

        if writer == None:
            self.basic2Text.AppendText(str(current_time + ' :  ' + msg + '\n'))
            with open(display_log, 'a') as d:
                d.write(str(current_time + ' :  ' + msg) + '\n')
        else:
            self.basic2Text.AppendText(str(msg + '\n'))

    def time_update(self, current):
        self.basic3Text.SetValue(current)

    def weather_update(self, weather):
        self.basic4Text.SetValue(weather)

    def writefiley(self):

        IP = self.Text1.GetValue()
        User = self.Text2.GetValue()
        PassWord = self.Text3.GetValue()
        file_path = self.basicText1.GetValue()
        keyBits = self.Text4.GetValue()
        CMbundle = self.basic5Text.GetValue()

        os.system('rm -rf %s' % pdca_file)
        string = "PDCAIP:" + str(IP) + '\n' + "PDCAAccount:" + str(User) + '\n' + "PDCAPassword:" + str(PassWord) \
                 + '\n' + "keyBits:" + str(keyBits) + '\n' + "list_file:" + str(file_path) + '\n' + "CMBundle:" + str(
            CMbundle)
        with open(pdca_file, 'a') as d:
            d.write(string + '\n')

    def OnIdle(self, event):
        self.count = self.count + 1
        if self.count >= 50:
            self.count = 0
            self.gauge.SetValue(self.count)

    def check_network(self, pdca, sina):
        if pdca == 1:
            self.network_one.SetBitmapLabel(self.img1)
        elif pdca == 0:
            self.network_one.SetBitmapLabel(self.img2)
        if sina == 1:
            self.network_two.SetBitmapLabel(self.img1)
        elif sina == 0:
            self.network_two.SetBitmapLabel(self.img2)

    def qsize_check(self, n):
        self.text_eight.SetLabel(str(n))


def read_log():
    if os.path.isfile(display_log):
        with open(display_log) as e:
            for line in e:
                wx.CallAfter(frame.basic2TextDisplay, line.replace('\n', ''), writer=False)


def check_log_row():
    while True:
        if os.path.isfile(display_log):
            number = commands.getoutput('cat -n < %s | awk \'{print$1}\' | tail -1' % display_log)
        else:
            number = "0"
        wx.CallAfter(frame.check_log, number)
        time.sleep(0.5)

def encode_file():
    os.system('%s %s %s %s' % (command_de_en_code, file_path, os.path.expanduser('~') + '/Downloads/encode.txt', '-e'))
    msg = "加密文件存储路径:" + os.path.expanduser('~') + '/Downloads/encode.txt'
    wx.CallAfter(frame.basic2TextDisplay, msg)


def decode_file():
    os.system('%s %s %s %s' % (command_de_en_code, file_path, os.path.expanduser('~') + '/Downloads/decode.txt', '-d'))
    msg = "解密文件存储路径:" + os.path.expanduser('~') + '/Downloads/decode.txt'
    wx.CallAfter(frame.basic2TextDisplay, msg)


def time_show():
    while True:
        current_time = time.strftime("%Y/%m/%d %H:%M:%S")
        wx.CallAfter(frame.time_update, current_time)
        show_weather()
        time.sleep(1)


def update_weather():
    '''
    :return:  100 秒更新一次天气情况，需要连接网络
    '''
    while True:
        get_weather(dir_path + '/file/wether1.csv', dir_path + '/file/wether2.csv')
        time.sleep(600)


def weather_start():
    thread.start_new(update_weather, ())


def show_weather():
    global msg_weather
    try:
        csv_read = open(dir_path + '/file/wether1.csv', 'r')
        reader = csv.DictReader(csv_read)

        a = []
        b = []
        c = []
        d = []
        e = []
        for i in reader:
            a.append(i['City'])
            b.append(i['Temp'])
            c.append(i['Update'])
            d.append(i['Weather'])
            # e.append(i['Prompt'])
            e.append(i['After 24h'])

        msg_weather = '[' + a[-1] + ']' + " |  更新时间: " + c[-1] + " | 天气：" + d[-1] + " | 温度: " + b[
            -1] + "℃" + "\n 未来24小时: " + e[-1]
        wx.CallAfter(frame.weather_update, msg_weather)
    except:
        msgs = "天气显示:  请连接互联网，并等待更新."
        wx.CallAfter(frame.weather_update, msgs)
        pass


def time_start_add():
    thread.start_new(time_show, ())


def get_crawl(url):
    '''
    :param url: 提供网络连接
    :return:    返回爬取得网页信息
    '''

    req = urllib2.Request(url)

    for i in range(6):

        if i == 5:
            print "-> 网页爬取失败,请检查网络连接."

        try:
            response = urllib2.urlopen(req, timeout=30).read()

        except:
            continue

        if response != None:
            break

    return response


def get_weather(weather_file, future_weather_file):
    '''
    :param url:                        基于网址: http://weather.sina.com.cn
    :param weather_file:               天气文件输出路径
    :param future_weather_file:        未来天气文件输出路径
    :return:
    '''

    url = 'http://weather.sina.com.cn'
    html = get_crawl(url)
    time_start = time.strftime("%m/%d/%Y_%H:%M:%S")

    # 检查天气情况文件是否存在
    if not os.path.isfile(weather_file):
        title = "Crawl time" + ',' + "City" + ',' + "Date" + ',' + "Update" + ',' + "Temp" + ',' + "Weather" + ',' + "Wind" + ',' \
                + "Humidity" + ',' + "Pollute" + ',' + "Sun_Up" + ',' + "Sun_Down" + ',' + "Remind" + ',' + "After 24h"  # + ',' + "Prompt"
        writefile(str(title), weather_file)
    if not os.path.isfile(future_weather_file):
        title_future = ["日期", "星期", "白天", "夜间", "温度", "风力", "污染", "程度"]
        write_csv(future_weather_file, title_future)

    # ---------------------------------------------------------------------------------------------------------------- #

    current_city = re.findall(r'<h4 class="slider_ct_name" id = "slider_ct_name" >(.*?)</h4>', html)
    current_date = re.findall(r'<p class="slider_ct_date">(.*?)</p>', html)
    update_time = re.findall(r'<div.*?更新时间.*?>(.*?)</div>', html)
    current_pollute = re.findall(
        r'<div .*?>\s*?<h6>(.*?)</h6>\s*?<p>(.*?)</p>\s*?</div>\s*?<div.*?>\s*?<p.*?>(.*?)</p>', html)
    current_time_point = re.findall(
        r'<span class="blk3_starrise">(.*?)</span>\s*?<span class="blk3_starfall">(.*?)</span>', html)
    # current_weather = re.findall(
    #    r'<div.*?>(.*?)&#8451;</div>\s*?<p.*?>\s*?(.*?)\&nbsp;\&nbsp;|\&nbsp;\&nbsp;\s*(\S*?)\&nbsp;\&nbsp;|\&nbsp;\&nbsp;'
    #    r'(.*?)</p>\s*?</div>\s*?<div.*?>\s*?<span class=".*?" data-tipid="." data-tipcont="(.*?)">\s*?<span.*?></span>',
    #    html)
    current_weather = re.findall(
        '<div .*?>(.*?)&#8451;</div>\s*?<p .*?>\s*?(.*?)&nbsp;&nbsp;|&nbsp;&nbsp;(.*?)&nbsp;&nbsp;|&nbsp;&nbsp;(.*?)</p>',
        html)

    print current_weather
    after_temp = re.findall(r'data-temp="(.*?)"', html)
    after_weather = re.findall(r'data-tempname="(.*?)"', html)

    current_prompt = re.findall(
        r'<div .*?>\s*?<h4>(.*?)</h4>\s*?<p>(.*?)</p>\s*?</div>\s*?<div .*?>\s*?<h4>(.*?)</h4>\s*?<p>(.*?)</p>\s*?'
        r'</div>\s*?<div .*?>\s*?<h4>(.*?)</h4>\s*?<p>(.*?)</p>\s*?</div>\s*?<div .*?>\s*?<h4>(.*?)</h4>\s*?<p>(.*?)</p>\s*?</div>',
        html)
    a, a1, b, b1, c, c1, d, d1 = current_prompt[0]

    e1 = str(a) + ': ' + str(a1)
    e2 = str(b) + ': ' + str(b1)
    e3 = str(c) + ': ' + str(c1)
    e4 = str(d) + ': ' + str(d1)

    eall = e1 + ' ' + e2 + ' ' + e3 + ' ' + e4

    city = current_city[0]
    date = current_date[0]
    update = update_time[0]

    return_list = []
    for i in current_weather:
        for j in i:
            h = re.findall(r'\S*', str(j).replace(' ', ''))
            if h[0] != "":
                return_list.append(str(h[0]))
    print return_list
    b1 = return_list[0]
    b2 = return_list[1]
    b3 = return_list[2]
    b4 = return_list[3]
    # b5 = return_list[4]

    m, e, f = current_pollute[0]
    ef = str(e) + ' | ' + str(f)

    start, end = current_time_point[0]

    a = str(after_temp[0]).replace(',', '*')
    d = str(after_weather[0]).replace(',', '*')

    result = str(time_start) + ',' + str(city) + ',' + str(date) + ',' + str(update) + ',' + str(b1) + ',' + str(b2) \
             + ',' + str(b3) + ',' + str(b4) + ',' + str(ef) + ',' + str(start) + ',' + str(
        end) + ',' + eall + ',' + d  # + ',' + str(b5)

    writefile(result, weather_file)

    # ---------------------------------------------------------------------------------------------------------------- #

    try:
        future_weather = re.findall(
            r'<p .*?>(.*?)</p>\s*?<p .*?>(.*?)</p>\s*?<p .*?>\s*?.*?</p>\s*?<p .*?>\s*?<span .*?>(.*?)</span>.*?<span .*?>(.*?)'
            r'</span>\s*?</p>\s*?<p .*?>(.*?)</p>\s*?<p .*?>(.*?)</p>\s*?<ul .*?>\s*?<li .*?>(.*?)</li>\s*?<li .*?>(.*?)</li>\s*?',
            html)

        if len(future_weather) > 0:
            for i in future_weather:
                list_result = []
                # list_result.append(str(time_start))
                a, b, c, d, e, f, g, h = i
                list_result.append(str(a))
                list_result.append(str(b))
                list_result.append(str(c))
                list_result.append(str(d))
                list_result.append(str(e))
                list_result.append(str(f))
                list_result.append(str(g))
                list_result.append(str(h))
                writer = csv.writer(open(future_weather_file, 'a'))
                writer.writerow(list_result)
    except IOError as e:
        print ('IOError', e)


def writefile(string, file):
    '''
    :param string:     输出文本内容
    :param file:       输出文件路径
    :return:           无返回
    '''
    try:
        with open(file, 'a') as d:
            d.write(string + '\n')
    except IOError as i:
        print ('IOError:', i)


def write_csv(file_path, content_list):
    '''
    :param content_list:     输出文本内容
    :param file_path:        输出文件路径
    :return:                 无返回
    '''
    try:
        writer = csv.writer(open(file_path, 'a'))
        writer.writerow(content_list)
    except IOError as e:
        print ('IOError:', e)


def futher_weather():
    try:
        list = []
        with open(dir_path + '/file/wether2.csv') as e:
            for line in e:
                list.append(str(line).replace('\n', ''))
        back_list = str(list[0]).replace(',', '  ') + str(list[-7]).replace(',', '  ') + str(list[-6]).replace(',',
                                                                                                               '  ') \
                    + str(list[-5]).replace(',', '  ') + str(list[-4]).replace(',', '  ') + str(list[-3]).replace(',',
                                                                                                                  '  ') \
                    + str(list[-2]).replace(',', '  ') + str(list[-1]).replace(',', '  ')
        wx.CallAfter(frame.basic2TextDisplay, '\n' + str(back_list))
    except:
        pass


def download_log():
    global logon_url
    global fpath

    Date = time.strftime("%Y_%m_%d_%H_%M_%S")
    fpath = os.path.expanduser('~') + '/Downloads/' + Date
    os.system('mkdir -p %s' % fpath)

    logon_url = "http://%s/cgi-bin/WebObjects/QCR.woa/wa/logon" % PDCAIPAdress

    ckeck_pdca = commands.getoutput('ping -c 1 -t 1 %s' % PDCAIPAdress)
    if "1 packets received" in ckeck_pdca:
        main()
    else:
        wx.CallAfter(frame.basic2TextDisplay, ckeck_pdca)


def read_info():
    global PDCAIPAdress
    global UserName
    global PassWord
    global formt
    global file_path
    global cm_bundle

    try:
        with open(pdca_file) as f:
            for line in f:
                if "PDCAIP:" in line:
                    PDCAIPAdress = str(line.split('PDCAIP:')[1]).replace('\n', '')
                if "PDCAAccount:" in line:
                    UserName = str(line.split('PDCAAccount:')[1]).replace('\n', '')
                if "PDCAPassword:" in line:
                    PassWord = str(line.split('PDCAPassword:')[1]).replace('\n', '')
                if "keyBits:" in line:
                    formt = str(line.split('keyBits:')[1]).replace('\n', '')
                if "list_file:" in line:
                    file_path = str(line.split('list_file:')[1]).replace('\n', '')
                if "CMBundle:" in line:
                    cm_bundle = str(line.split('CMBundle:')[1]).replace('\n', '')
    except:
        pass


def read_list(file):
    serial_number_list = []
    with open(file) as f_job:
        for line in f_job:
            sn = re.findall(r'C02[A-Z].{8}', line)
            if len(sn) > 0:
                serial_number_list.append(sn[0])

        return serial_number_list


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
            print "Logon QCR Fail."
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
            print "FAIL redirect to product history page."
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
            print "%s -> ERROR, FAIL to search find this SN on PDCA" % (serial_number)
            # frame.displayinfo(msg)
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
            print "%s -> ERROR, FAIL to search find this SN Log on PDCA" % (serial_number)
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
            print "%s -> ERROR, The last page Fail." % (serial_number)
            # frame.displayinfo(msg)
            os._exit(1)
        try:
            last_crawl = urllib2.urlopen(fourth_url, timeout=30).read()
        except:
            continue

        if re.search(r'<a href="(.*?)" name=".*?"><img', last_crawl):
            break
    sys.stdout.flush()
    mylock.release()
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
    frame.show_start_or_fail(1)
    mylock.acquire()
    meg1 = "> Starting  - [" + str(job) + "]" + " - Thread@ " + str(worktype)
    wx.CallAfter(frame.basic2TextDisplay, meg1)
    crawl_sitemap(job)
    meg2 = "> Finished  - [" + str(job) + "]" + " - Thread@ " + str(worktype)
    frame.qsize_check(q.qsize())
    wx.CallAfter(frame.basic2TextDisplay, meg2)
    if q.qsize() == 0:
        wx.CallAfter(frame.basic2TextDisplay, "下载完成. Log 存放路径: " + fpath)
        frame.show_start_or_fail(0)


def Explain():
    with open(dir_path + '/file/Explain.txt') as p:
        for line in p:
            wx.CallAfter(frame.basic2TextDisplay, str(line).replace('\n', ''))


def find_file(path, formet):
    try:
        a = []
        fns = [os.path.join(root, fn) for root, dirs, files in os.walk(path) for fn in files]
        for f in fns:
            if os.path.isfile(f):
                if formet in f:
                    a.append(f)
        return a
    except IOError as o:
        print ('IOError', o)


def for_download_log_check():
    Date = time.strftime("%Y_%m_%d_%H_%M_%S")
    result_path = os.path.expanduser('~') + '/Downloads/' + Date + '.csv'

    if not os.path.isfile(result_path):
        string = "Time" + ',' + "Serial Number" + ',' + "WIP" + ',' + "Test Bundle" + ',' + "CM Bundle" + ',' + 'Partition Time' + ',' + 'Test Bundle Time' \
                 + ',' + 'CM Copy Time' + ',' + "Download Time" + ',' + "ASR bandwidth" + ',' + "CM Copy bandwitdth"
        writefile(string, result_path)

    a = find_file(file_path, ".gz")
    frame.show_start_or_fail(1)
    for h in a:
        q.put(h)
    for i in range(q.qsize()):
        try:
            filepath = q.get()
            os.system('gunzip %s &>/dev/null' % (filepath))
            filename = filepath.replace('.gz', '')
            SerialNumber = str(filename).split('/')[-1].split('_')[0]
            download_log_check(filename, SerialNumber, result_path)
            os.system('rm -rf %s' % filename)
            frame.qsize_check(q.qsize())
            wx.CallAfter(frame.basic2TextDisplay, "Processing  [" + SerialNumber + "]")
            if q.qsize() == 0:
                wx.CallAfter(frame.basic2TextDisplay, "处理完成, 结果存储路径: " + result_path)
                frame.show_start_or_fail(0)
        except:
            pass
    frame.show_start_or_fail(0)


# ----------------------------------------------------------------------------------------------------------------------#
# for runin time check
def Time_chek(_time):
    try:
        timeArray = time.strptime(_time, "%Y/%m/%d %H:%M:%S")
        timeStamp = int(time.mktime(timeArray))
        return timeStamp
    except UnboundLocalError as p:
        print ('UnboundLocalError', p)


def Time_calculate(Start, End):
    d = int(End) - int(Start)
    hour = d / 3600
    d1 = d % 3600
    min = d1 / 60
    d2 = d1 % 60
    time = str(hour) + "h" + str(min) + "m" + str(d2) + "s"
    return time


def config_check(path):
    try:
        K = "Apple Internal Keyboard / Trackpad"
        with open(path) as fe:
            for line in fe:
                if K in line:
                    KB = line.split('"')[3]
                if "Memory" in line:
                    MY = line.split('"')[1]
                if "devicecapacity" in line:
                    SD = line.split('"')[1]
                    if SD == 1000:
                        SD = 1024
                if "frequency" in line:
                    CPU = line.split('"')[3]
            return CPU, MY, SD, KB
    except TypeError as po:
        print ('TypeError', po)


def for_runin_time_check():
    Date = time.strftime("%Y_%m_%d_%H_%M_%S")
    result_path = os.path.expanduser('~') + '/Downloads/' + Date + '.csv'

    if not os.path.isfile(result_path):
        string = "Serial Number," + 'CPU,' + "Memory," + "SSD," + "Contry Code," + \
                 "Start Time," + "End Time," + "Left Time," + "Test Bundle," + "MemoryVendor"
        writefile(string, result_path)

    start_parameter = "CM_Bundle_Verify"
    end_parameter = "CM ASR _694"

    a = find_file(file_path, ".tgz")
    frame.show_start_or_fail(1)
    for h in a:
        q.put(h)
    for i in range(q.qsize()):
        try:
            file_path_road = q.get()
            filepath = os.path.dirname(file_path_road)
            os.system('cd %s ; tar -zxf %s &>/dev/null' % (filepath, file_path_road))
            FileName = file_path_road.replace('.tgz', '')
            SerialNumber = str(file_path_road).split('/')[-1].split('_')[0]
            r = glob.glob(FileName + '/*/processlog.plog')
            t = glob.glob(FileName + '/*/*/processlog.plog')
            if r:
                LogPoath = r[0]
            if t:
                LogPoath = t[0]

            runin_time_check(SerialNumber, LogPoath, start_parameter, end_parameter, FileName, result_path)
            os.system('rm -rf %s' % FileName)
            frame.qsize_check(q.qsize())
            wx.CallAfter(frame.basic2TextDisplay, "Processing  [" + SerialNumber + "]")
            if q.qsize() == 0:
                wx.CallAfter(frame.basic2TextDisplay, "处理完成, 结果存储路径: " + result_path)
                frame.show_start_or_fail(0)

        except:
            pass
    frame.show_start_or_fail(0)


def runin_time_check(SerialNumber, LogPoath, start_parameter, end_parameter, Temproad, result_path):
    try:
        time_start = []
        time_end = []
        c = []
        b = []
        with open(LogPoath) as e:
            for line in e:
                if start_parameter in line:
                    Time1 = re.findall(r'[0-9]{4}/[0-9]{2}/[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}', line)
                    if len(Time1) > 0:
                        time_start.append(Time1[0])
                if end_parameter in line:
                    Time2 = re.findall(r'[0-9]{4}/[0-9]{2}/[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}', line)
                    if len(Time2) > 0:
                        time_end.append(Time2[0])
                if "Memory" in line and "vendor:" in line:
                    c.append(line.split('"')[11].split(':')[-1])
                if "DTI" in line:
                    ad = line.split('"')[15]
                    b.append(ad)

        ConfigFile = find_file(Temproad, "configExpected.txt")
        CPU, Memory, SSD, Keyboard = config_check(ConfigFile[0])

        if c:
            memoryvonder = c[0]
        else:
            memoryvonder = "none"

        if len(b) > 0:
            bundle_name = b[1]
        else:
            bundle_name = "none"

        time_left = Time_calculate(Time_chek(time_start[-1]), Time_chek(time_end[-1]))

        result_info = str(SerialNumber) + ',' + str(CPU) + ',' + str(Memory) + ',' + str(SSD) + ',' + str(
            Keyboard) + ',' + \
                      str(time_start[-1]) + ',' + str(time_end[-1]) + ',' + str(time_left) + ',' + str(
            bundle_name) + ',' + str(memoryvonder)
        writefile(result_info, result_path)

    except:
        pass


# ----------------------------------------------------------------------------------------------------------------------#
# Bundle Download
def check_extend_disk():
    msg = commands.getoutput('diskutil list')  # diskutil list external
    wx.CallAfter(frame.basic2TextDisplay, '\n' + msg)


def Special_Command(set_cmd, passwd):
    '''
    :param set_cmd: 给定命令行，然后跑，给的命令一般都要是需要在root权限下才能跑得，不然用这格式就没什么意义了
                    直接可以用os.system或者commands.getoutput就可以了
    :return: 没有返回值
    '''
    ret = ""
    try:
        foo = pexpect.spawn('%s' % set_cmd)
        foo.expect('.assword:*')
        foo.sendline(passwd)
        ret = foo.read()
        foo.interact()
    except:
        pass
    return ret


def for_bundle_download():
    # global file_path    test bundle 文件
    # global formt        外接盘
    # global PassWord     本机电脑密码
    # global cm_bundle    CM bundle 文件

    path = os.path.expanduser('~')
    testbundlepath = find_file(path, file_path)
    cmbundlepath = find_file(path, cm_bundle)

    cmd1 = 'sudo diskutil partitionDisk /dev/%s 1 GPTFormat HFS+ Diagnostics 1G' % formt
    cmd2 = 'sudo /usr/sbin/asr -partition /dev/%s -testsize 70g -retestsize 1g -recoverysize 80g' % formt
    cmd3 = 'sudo diskutil unmountDisk /dev/%s' % formt
    cmd4 = '/usr/sbin/asr -s %s -t /dev/%s3 -erase -noprompt' % (testbundlepath, formt)
    cmd5 = 'diskutil mountDisk /dev/%s3' % formt
    cmd6 = 'sudo ditto -rsrcFork %s /Volumes/MaxDisk' % cmbundlepath


def net_work_check():
    while True:
        thread.start_new(net_check, ())
        time.sleep(3)


def net_check():
    ckeck_pdca = commands.getoutput('ping -c 1 -t 1 17.239.64.36')
    check_sina = commands.getoutput('ping -c 1 -t 1 weather.sina.com.cn')
    if "1 packets received" in ckeck_pdca:
        pdca = 1
    else:
        pdca = 0
    if "1 packets received" in check_sina:
        sina = 1
    else:
        sina = 0
    frame.check_network(pdca, sina)


# ----------------------------------------------------------------------------------------------------------------------#
def speak_weather():
    wx.CallAfter(frame.basic2TextDisplay, '\n' + str(msg_weather).replace('|', ','))
    os.system('say %s' % str(msg_weather).replace('|', '。'))


def download_log_check(filename, SerialNumber, result_path):
    with open(filename) as ae:
        try:
            BundleName = "None"
            CMBundle = "None"
            TimeStart = "None"
            TotalTime = "None"
            WIP = "None"
            Partition = "None"
            Test_time = "None"
            CM_time = "None"
            ASR_bandwidth = "None"
            CM_bandwidth = "None"
            for line in ae:
                if ".dmg" in line and "J79A" in line:
                    BundleName = line.split('/')[-1].split('.dmg')[0]
                d = re.findall(r'\[.*\.dmg\]', line)
                if d:
                    CMBundle = d[0].split('[')[2].replace(']', '')
                t = re.findall(
                    r'201[0-9]-[0-9][0-9]-[0-9][0-9] \[[0-9][0-9]\:[0-9][0-9]\:[0-9][0-9]\.[0-9][0-9][0-9]\]', line)
                if t:
                    TimeStart = t[0]  # .split('.')[0].replace('[','')
                if "Overall" in line:
                    TotalTime = line.split('=')[1]
                if "Partition =" in line:
                    Partition = line.split('=')[1]
                if "Test Image Restore =" in line:
                    Test_time = line.split('=')[1]
                if "CM Copy =" in line:
                    CM_time = line.split('=')[1]
                if "ASR bandwidth =" in line:
                    ASR_bandwidth = line.split('=')[1]
                if "CM Copy bandwitdth =" in line:
                    CM_bandwidth = line.split('=')[1]
                w = re.findall(r'C02.*\+.*\"', line)
                if w:
                    WIP = w[0].replace('"', '')
            result = str(TimeStart).replace('\n', '') + ',' + str(SerialNumber).replace('\n', '') + ',' + str(
                WIP).replace('\n', '') + ',' + str(BundleName).replace('\n', '') + ',' + str(
                CMBundle).replace('\n', '') + ',' + str(Partition).replace('\n', '') + ',' + str(Test_time).replace(
                '\n', '') \
                     + ',' + str(CM_time).replace('\n', '') + ',' + str(TotalTime).replace('\n', '') + ',' + \
                     str(ASR_bandwidth).replace('\n', '') + ',' + str(CM_bandwidth).replace('\n', '')
            writefile(str(result), result_path)
        except UnboundLocalError as e:
            print('UnboundLocalError', e)


def main():
    global startsize
    os.system('mkdir -p %s' % fpath)

    sn_list = read_list(file_path)
    star = "Begin...."
    wx.CallAfter(frame.weather_update, star)

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
