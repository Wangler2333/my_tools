#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# __author__: Saseny Zhou
# Created on 2017/08/08 witsh the first version
# 目标数据爬取网站 12306 官网


import urllib
import urllib2
import urllib3
import requests
import scrapy
import lxml
import wx
import re
import wx.grid
from bs4 import BeautifulSoup
import plistlib
import os
import sys
import threading
import thread
import time

dir_path = os.path.dirname(sys.argv[0]) + '/File/'


class Frame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, "Train", size=(1430, 800), style=wx.DEFAULT_FRAME_STYLE)
        panel = wx.Panel(self, -1)

        font = wx.Font(10, wx.DECORATIVE, wx.NORMAL, wx.NORMAL, False, 'Courier New')
        self.SetFont(font)

        self.basicText1 = wx.TextCtrl(panel, -1, "1111111111111111111", size=(200, -1), pos=(5, 10), style=wx.TE_LEFT)

#'''
        self.grid = wx.grid.Grid(self, size=(1300, 560), pos=(20, 200))
        self.grid.CreateGrid(50, 17)
        self.grid.SetRowLabelSize(30)
        self.grid.SetColLabelSize(30)
        self.grid.SetColSize(5, 5)
        self.grid.SetRowSize(5, 5)

        item_list = ['查询日期', '车次', '列车起点-终点', '起点-终点', '开车时间', '到达时间', '历时', '商务座/特等座', '一等座', '二等座', '高级软卧', '软卧',
                     '动铺', '硬卧', '软座', '硬座', '无座']

        count = 0
        for i in item_list:
            self.grid.SetColLabelValue(count, i)
            count = count + 1
        self.grid.SetCellValue(0, 0, '')

        # grid.SetCellSize(5, 5, 5, 5)   # 设置中间区域合并单元格
        # for row in range(5):
        #    for col in range(5):
        #        grid.SetCellValue(row, col, "%s%s" % ("", ""))

    def set_values(self, list):
        a = 0
        for i in list:
            b = 0
            for l in i:
                self.grid.SetCellValue(a, b, l)
                b = b + 1
            a = a + 1
#'''

def getTrain_list():
    url = 'https://kyfw.12306.cn/otn/resources/js/query/train_list.js?scriptVersion=1.0'
    try:
        requests.adapters.DEFAULT_RETRIES = 5
        response = requests.get(url, stream=True, verify=False)
        status = response.status_code
        if status == 200:
            with open(dir_path + 'train_list.txt', 'wb') as of:
                for chunk in response.iter_content(chunk_size=102400):
                    if chunk:
                        of.write(chunk)
    except requests.ConnectionError as e:
        print ('requests.ConnectionError', e)


def trainListStartToEnd():
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


def read_plist():
    return plistlib.readPlist(dir_path + 'trainList.plist')


def getstationcode():
    url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9002'
    try:
        requests.adapters.DEFAULT_RETRIES = 5
        response = requests.get(url, stream=True, verify=False)
        status = response.status_code
        if status == 200:
            with open(dir_path + 'stationcode.txt', 'wb') as of:
                for chunk in response.iter_content(chunk_size=102400):
                    if chunk:
                        of.write(chunk)
    except requests.ConnectionError as e:
        print ('requests.ConnectionError', e)


def processstationcode():
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


def train_number_search(train_number):
    over_all = read_plist()
    for i in over_all.keys():
        if train_number == i:
            print i, over_all[i]['route'], over_all[i]['train_no']


def full_station_search(start, end):
    over_all = read_plist()
    for i in over_all.items():
        if start in str(i[1]['route'].encode('utf-8')).split('-')[0] and end in \
                str(i[1]['route'].encode('utf-8')).split('-')[1]:
            print i[0], i[1]['route'], i[1]['train_no']


def start_station_search(start):
    over_all = read_plist()
    for i in over_all.items():
        if start in str(i[1]['route'].encode('utf-8')).split('-')[0]:
            print i[0], i[1]['route'], i[1]['train_no']


def end_station_search(end):
    over_all = read_plist()
    for i in over_all.items():
        if end in str(i[1]['route'].encode('utf-8')).split('-')[1]:
            print i[0], i[1]['route'], i[1]['train_no']


def getticketinfo(date, from_station, to_station):
    url = 'https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date=%s&leftTicketDTO.from_station=%s&leftTicketDTO.to_station=%s&purpose_codes=ADULT' % (
        date, from_station, to_station)
    break_down = 0
    for o in range(10):
        try:
            requests.adapters.DEFAULT_RETRIES = 5
            response = requests.get(url, stream=True, verify=False)
            status = response.status_code
            if status == 200:
                with open(dir_path + 'tichetinfo.txt', 'wb') as of:
                    for chunk in response.iter_content(chunk_size=102400):
                        if chunk:
                            if from_station in chunk or to_station in chunk:
                                break_down = 1
                            of.write(chunk)
            if break_down == 1:
                break
        except:
            continue


def analyse_ticketinfo():
    with open(dir_path + 'tichetinfo.txt') as b:
        text = b.readline()
        tt = text.decode("utf-8")
        ss = tt.split('[')[1].split(']')[0].replace(',', '\n').split('\n')
        ad = '|预订'
        for i in ss:
            # print i
            if ad.decode('utf-8') in i:
                print i.split(ad.decode('utf-8'))[1]


# train_number_search('D22')
# full_station_search('上海虹桥', '青岛')
# start_station_search('上海虹桥')
# end_station_search('邵阳')
# getstationcode()
# processstationcode()
# getticketinfo('2017-08-19','SHH','CSQ')
# getTrain_list()
# trainListStartToEnd()
#analyse_ticketinfo()

thread.start_new(analyse_ticketinfo,())
thread.exit()

# '''
if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = Frame()
    frame.Show(True)
    app.MainLoop()
# '''
