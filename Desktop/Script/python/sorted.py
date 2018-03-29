#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# __author__: Saseny Zhou


import wx
import sys, os
from wx.lib.mixins.listctrl import ColumnSorterMixin
import plistlib
import thread
import time

actresses = {
    '1' : ('jessica alba', 'pomona', '1981', '2'),
    '2' : ('sigourney weaver', 'new york', '1949',''),
    '3' : ('angelina jolie', 'los angeles', '1975',''),
    '4' : ('natalie portman', 'jerusalem', '1981',''),
    '5' : ('rachel weiss', 'london', '1971',''),
    '6' : ('scarlett johansson', 'new york', '1984','')
}

auto_file = os.path.dirname(sys.argv[0]) + '/parameter.plist'


class SortedListCtrl(wx.ListCtrl, ColumnSorterMixin):
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, -1, style=wx.LC_REPORT)
        ColumnSorterMixin.__init__(self, len(actresses))
        self.itemDataMap = actresses

    def GetListCtrl(self):
        return self


class Actresses(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(580, 230))

        hbox = wx.BoxSizer(wx.HORIZONTAL)

        panel = wx.Panel(self, -1)

        self.list = SortedListCtrl(panel)

        self.list.InsertColumn(0, '名字', width=140)
        self.list.InsertColumn(1, '地点', width=130)
        self.list.InsertColumn(2, '年份', wx.LIST_FORMAT_RIGHT, 90)
        self.list.InsertColumn(3, '其他', wx.LIST_FORMAT_RIGHT, 90)


        hbox.Add(self.list, 1, wx.EXPAND)
        panel.SetSizer(hbox)

        items = self.readplist().items()

        for key, data in items:
            index = self.list.InsertItem(sys.maxint, '\t\t' + data[0])
            self.list.SetItem(index, 1, data[1])
            self.list.SetItem(index, 2, data[2])
            self.list.SetItem(index, 3, data[3])
            self.list.SetItemData(index, int(key))

        #thread.start_new(self.display_info,())

        self.Centre()
        self.Show(True)

    def display_info(self):
        while True:

            items = self.readplist().items()

            self.list.ClearAll()

            time.sleep(5)



            for key, data in items:
                index = self.list.InsertItem(sys.maxint, '\t\t' + data[0])
                self.list.SetItem(index, 1, data[1])
                self.list.SetItem(index, 2, data[2])
                self.list.SetItem(index, 3, data[3])
                self.list.SetItemData(index, int(key))

            self.list.RefreshItem(1)

    def writeplist(self):
        plistlib.writePlist(actresses, auto_file)

    def readplist(self):
        return plistlib.readPlist(auto_file)


app = wx.App()
Actresses(None, -1, 'actresses')
app.MainLoop()
