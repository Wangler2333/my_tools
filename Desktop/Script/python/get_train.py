#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# __author__: Saseny Zhou

import wx
import requests
import re
import os, sys
import plistlib
import matplotlib as pl
import thread
import threading
import Queue
import wx.lib.buttons as buttons
import time


q = Queue.Queue(0)

# import daemon


dir_path = os.path.dirname(sys.argv[0]) + '/File/'


class train_get(object):
    '''
       处理 12306 列车数据的类，得到所有列车信息以及站别代码
       抓取 特定时间特定站点的车票数据
          -- 根据时间，起点到终点站别查询信息
          -- 根据车次，时间查询信息
    '''

    def __init__(self, search_date=None, from_station=None, to_station=None, train_number=None):
        self.date = search_date
        self.start_before = from_station
        self.target_before = to_station
        self.number = train_number

    def search_station_code(self):
        over_all = self.read_station_code()
        for i in over_all.keys():
            if self.start_before.decode('utf-8') == i:
                self.start = over_all[i]
            if self.target_before.decode('utf-8') == i:
                self.target = over_all[i]

    def search_station_name(self, code):
        over_all = self.read_station_code()
        for i in over_all.items():
            if code == i[1]:
                return i[0]

    def get_train_list(self):
        train_list_url = 'https://kyfw.12306.cn/otn/resources/js/query/train_list.js?scriptVersion=1.0'
        try:
            requests.adapters.DEFAULT_RETRIES = 5
            response = requests.get(train_list_url, stream=True, verify=False)
            status = response.status_code
            if status == 200:
                with open(dir_path + 'train_list.txt', 'wb') as of:
                    for chunk in response.iter_content(chunk_size=102400):
                        if chunk:
                            of.write(chunk)
        except requests.ConnectionError as e:
            print ('requests.ConnectionError', e)

    def train_list_check(self):
        if not os.path.isfile(dir_path + 'train_list.txt'):
            self.get_train_list()
        try:
            with open(dir_path + 'train_list.txt', 'rb') as of:
                text = of.readline()
                tt = text.decode("utf-8")
                ss = tt.replace("},{", "}\n{").replace("2017-", "\n").replace("[", "\n").split("\n")
                m_list = {}
                for s in ss:
                    a = re.findall(r'station_train_code":"(.*?)","train_no":"(.*?)"', s)
                    if a:
                        if "(" in a[0][0]:
                            train_number = a[0][0].split('(')[0]
                            route = a[0][0].split('(')[1].split(')')[0]
                            train_no = a[0][1]
                            m_list[train_number] = {'route': route, 'train_no': train_no}
            plistlib.writePlist(m_list, dir_path + 'trainList.plist')
            os.system('rm -rf %s' % dir_path + 'train_list.txt')
        except TypeError as e:
            print ('TypeError:', e)

    def get_station_code(self):
        station_code_url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9002'
        try:
            requests.adapters.DEFAULT_RETRIES = 5
            response = requests.get(station_code_url, stream=True, verify=False)
            status = response.status_code
            if status == 200:
                with open(dir_path + 'stationcode.txt', 'wb') as of:
                    for chunk in response.iter_content(chunk_size=102400):
                        if chunk:
                            of.write(chunk)
        except requests.ConnectionError as e:
            print ('requests.ConnectionError', e)

    def station_code_check(self):
        if not os.path.isfile(dir_path + 'stationcode.txt'):
            self.get_station_code()
        list = {}
        with open(dir_path + 'stationcode.txt') as of:
            text = of.readline()
            tt = text.decode("utf-8")
            ss = tt.replace('@', '\n').split('\n')
            for i in ss:
                all_code = re.findall(r'\|(.*?)\|([A-Z]*)\|', i)
                if len(all_code) > 0:
                    station, code = all_code[0]
                    list[station] = code
        plistlib.writePlist(list, dir_path + 'stationcode.plist')
        os.system('rm -rf %s' % dir_path + 'stationcode.txt')

    def get_ticket_info(self):
        self.search_station_code()
        ticket_info_url = 'https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date=%s&leftTicketDTO.from_station=%s&leftTicketDTO.to_station=%s&purpose_codes=ADULT' % (
            self.date, self.start, self.target)
        # print ticket_info_url
        break_down = 0
        for o in range(10):
            try:
                requests.adapters.DEFAULT_RETRIES = 5
                response = requests.get(ticket_info_url, stream=True, verify=False)
                status = response.status_code
                if status == 200:
                    with open(dir_path + 'ticket_info.txt', 'wb') as of:
                        for chunk in response.iter_content(chunk_size=102400):
                            if chunk:
                                if self.start in chunk or self.target in chunk:
                                    break_down = 1
                                of.write(chunk)
                if break_down == 1:
                    break
            except:
                continue

    def read_train_list_plist(self):
        if not os.path.isfile(dir_path + 'trainList.plist'):
            self.train_list_check()
        return plistlib.readPlist(dir_path + 'trainList.plist')

    def read_station_code(self):
        if not os.path.isfile(dir_path + 'stationcode.plist'):
            self.station_code_check()
        return plistlib.readPlist(dir_path + 'stationcode.plist')

    def train_number_search(self):
        over_all = self.read_train_list_plist()
        search_result = []
        for i in over_all.keys():
            if self.number == i:
                al = i, over_all[i]['route'], over_all[i]['train_no']
                search_result.append(al)
        return search_result

    def full_station_search(self):
        over_all = self.read_train_list_plist()
        search_result = []
        for i in over_all.items():
            if self.start in str(i[1]['route'].encode('utf-8')).split('-')[0] and self.target in \
                    str(i[1]['route'].encode('utf-8')).split('-')[1]:
                al = i[0], i[1]['route'], i[1]['train_no']
                search_result.append(al)
        return search_result

    def start_station_search(self):
        over_all = self.read_train_list_plist()
        search_result = []
        for i in over_all.items():
            if self.start in str(i[1]['route'].encode('utf-8')).split('-')[0]:
                al = i[0], i[1]['route'], i[1]['train_no']
                search_result.append(al)
        return search_result

    def end_station_search(self):
        over_all = self.read_train_list_plist()
        search_result = []
        for i in over_all.items():
            if self.target in str(i[1]['route'].encode('utf-8')).split('-')[1]:
                al = i[0], i[1]['route'], i[1]['train_no']
                search_result.append(al)
        return search_result

    def ticket_info_check(self):
        if not os.path.isfile(dir_path + 'ticket_info.txt'):
            self.get_ticket_info()
        search_result = {}
        n = 0
        try:
            with open(dir_path + 'ticket_info.txt') as e:
                text = e.readline()
                tt = text.decode("utf-8")
                ss = tt.replace(',', '').replace(':', '').replace('\"', '\n').split('\n')
                for i in ss:
                    if i != "" and '|' in i:
                        n = n + 1
                        info = i.split('|')

                        if info[-4] == "" and info[-11] == "":
                            ad = ""
                        elif info[-4] != "" and info[-11] == "":  # 商务座特等座
                            ad = info[-4]
                        elif info[-4] == "" and info[-11] != "":
                            ad = info[-11]

                        search_result[n] = {
                            '是否可购票': info[1],  # 预定/2300-0600系统维护时间
                            '车次': info[3],  # 车次
                            '列车起点': self.search_station_name(info[4]),  # 起点
                            '列车终点': self.search_station_name(info[5]),  # 终点
                            '选择起点': self.search_station_name(info[6]),  # 选择起点
                            '选择终点': self.search_station_name(info[7]),  # 选择终点
                            '开车时间': info[8],  # 开车时间
                            '到达时间': info[9],  # 到达时间
                            '耗时': info[10],  # 耗时
                            'Yes/No': ad,  # IS_TIME_NOT_BUY
                            '选择日期': info[13],  # 选择时间
                            '商务座特等座': info[-11],  # 商务座特等座 （部分）
                            '一等座': info[-5],  # 一等座
                            '二等座': info[-6],  # 二等座
                            '硬座': info[-7],  # 硬座
                            '硬卧': info[-8],  # 硬卧
                            '无座': info[-10],  # 无座
                            '动卧': info[-3],  # 动卧
                            '软卧': info[-13],  # 软卧
                            '高级软卧': info[-15],  # 高级软卧
                        }
            os.system('rm -rf %s' % (dir_path + 'ticket_info.txt'))
            return search_result
        except TypeError as e:
            print ('TypeError:', e)

    def from_train_number_check_tichet(self):
        a, info, b = self.train_number_search()[0]
        self.start_before = str(info.encode('utf-8')).split('-')[0]
        self.target_before = str(info.encode('utf-8')).split('-')[1]
        search_result = self.ticket_info_check()
        return search_result


class Frame(wx.Frame):
    '''
        GUI 类, 设置各类GUI控件
    '''

    def __init__(self):

        # 建立一个窗口，窗口大小 (1300 x 850)  设置默认格式
        wx.Frame.__init__(self, None, -1, "Train Info Search", size=(1300, 850), style=wx.DEFAULT_FRAME_STYLE)
        panel = wx.Panel(self, -1)

        # 建立字体格式，字体大小以及显示状态  -- 字体
        font = wx.Font(50, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False, 'Courier New')
        self.SetFont(font)

        # 静态显示label，以及动态输入显示框  -- 车次
        self.label_one = wx.StaticText(panel, -1, "车次:", pos=(30, 53), style=wx.TE_LEFT)
        self.text_one = wx.TextCtrl(panel, -1, "", size=(50, 25), pos=(65, 50), style=wx.TE_LEFT)

        # 中间大型输出框，设置格式仅读不可写  -- 输出框
        self.label_two = wx.StaticText(panel, -1, "结果输出:", pos=(30, 180), style=wx.TE_LEFT)
        self.text_two = wx.TextCtrl(panel, -1, "", size=(1240, 600), pos=(30, 200),
                                    style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH)

        # 静态显示label，以及动态输入显示框  -- 日期
        self.label_three = wx.StaticText(panel, -1, "日期:", pos=(30, 83))
        self.text_three = wx.TextCtrl(panel, -1, "", size=(90, 25), pos=(65, 80), style=wx.TE_LEFT)

        # 静态显示label，以及动态输入显示框  -- 起点站
        self.label_four = wx.StaticText(panel, -1, "起点:", pos=(170, 83))
        self.text_four = wx.TextCtrl(panel, -1, "", size=(80, 25), pos=(210, 80), style=wx.TE_LEFT)

        # 静态显示label，以及动态输入显示框  -- 终点站
        self.label_five = wx.StaticText(panel, -1, "终点:", pos=(300, 83))
        self.text_five = wx.TextCtrl(panel, -1, "", size=(80, 25), pos=(340, 80), style=wx.TE_LEFT)

        # 静态显示label，以及动态输入显示框  -- 循环次数
        self.label_six = wx.StaticText(panel, -1, "循环次数:", pos=(450, 83))
        self.text_six = wx.TextCtrl(panel, -1, "", size=(50, 25), pos=(515, 80), style=wx.TE_LEFT)

        # 静态显示label，以及动态输入显示框  -- 其他
        self.label_seven = wx.StaticText(panel, -1, "其他:", pos=(30, 133))
        self.text_seven = wx.TextCtrl(panel, -1, "", size=(500, 25), pos=(65, 130), style=wx.TE_LEFT)
        self.text_seven.SetInsertionPoint(0)

        # 功能选择框
        self.sampleList = ['空选项', '余票查询', '等待更新', '等待更新', '等待更新', '等待更新', '等待更新', '等待更新', '等待更新', '等待更新', '等待更新']
        self.checkbox = wx.RadioBox(panel, -1, '功能选择栏(单选)', (600, 25), wx.DefaultSize, self.sampleList, 4,
                                    wx.RA_SPECIFY_COLS)

        # 开始按钮
        self.button = buttons.GenButton(panel, -1, 'Start', size=(180, 90), pos=(1050, 60))
        self.button.SetFont(wx.Font(20, wx.SWISS, wx.NORMAL, wx.BOLD, False))
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.button)
        self.button.SetDefault()
        self.button.SetBezelWidth(5)

        # 设置背景颜色
        self.button.SetBackgroundColour('Green')
        # self.SetBackgroundColour('yellow')
        self.SetForegroundColour('white')
        # self.text_two.SetBackgroundColour('Grey')
        self.checkbox.SetBackgroundColour('Grey')
        # self.label_three.SetForegroundColour('Red')

        # 状态显示条
        self.pass_bmp = wx.Image(dir_path + '/png/' + 'pass.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        self.fail_bmp = wx.Image(dir_path + '/png/' + 'fail.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        self.states_show = wx.BitmapButton(panel, -1, self.fail_bmp, size=(280, 35), pos=(665, 128))

        self.count = 0

    def OnClick(self, event):
        a,b,c,d,e,f = self.get_input_parameter()
        self.count = self.count + 1

        thread.start_new(running, (e,))

        if self.count % 2 != 0:
            self.show_states(1)
            self.show_start_or_fail(1)


        elif self.count % 2 == 0:
            self.show_states(0)
            self.show_start_or_fail(0)
        print self.count

    def get_input_parameter(self):
        '''
        :return:  读取所有text读取到的值
        '''
        self.a = self.text_one.GetValue()  # 车次
        self.b = self.text_three.GetValue()  # 日期
        self.c = self.text_four.GetValue()  # 起点
        self.d = self.text_five.GetValue()  # 终点
        self.e = self.text_six.GetValue()  # 循环次数
        self.f = self.text_seven.GetValue()  # 其他

        return self.a,self.b,self.c,self.d,self.e,self.f

    def show_states(self, states):
        '''
        :param states: 给定需要的状态值，1代表绿色，0代表红色
        :return:       更改中间显示条的颜色
        '''
        if states == 1:
            self.states_show.SetBitmapLabel(self.pass_bmp)
        elif states == 0:
            self.states_show.SetBitmapLabel(self.fail_bmp)

    def show_start_or_fail(self, a):
        '''
        :param a:      给定需要的状态值，1代表绿色，0代表红色
        :return:       更改开始按钮显示的颜色
        '''
        if a == 1:
            self.button.SetBackgroundColour('Red')
            self.button.SetLabel('Running')
        elif a == 0:
            self.button.SetBackgroundColour('Green')
            self.button.SetLabel('Start')

    def display_result(self, msg):
        '''
        :param msg:    提供需要输出的信息
        :return:       输出所提供的信息
        '''
        self.text_two.AppendText(msg)  # + '\n')


def running(cycle_count):
    count = 0
    print cycle_count
    while [ count <= cycle_count ]:
        count = count + 1
        print count
        msg = '甄茂磊二傻子'
        wx.CallAfter(frame.display_result, msg)
        time.sleep(1)



'''
a = train_get(search_date='2017-08-21',train_number='Z247')

# a.tichet_info_check()
# a.search_station_name()
# a.train_list_check()

e = '车次'
d = '二等座'

for i in a.tichet_info_check().values():
    print i[e],i[d]


while True:
    d = a.train_number_search()[0]

    print a.number
    for i in a.from_train_number_check_tichet().values():
        if a.number in i['车次']:
            print i['车次'],i['软卧'],i['硬卧'],i['硬座'],i['无座']
    print d[0],d[1],d[2]
'''

if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = Frame()
    frame.Show()
    app.MainLoop()
