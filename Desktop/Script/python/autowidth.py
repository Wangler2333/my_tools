#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# __author__: Saseny Zhou


import wx
import sys
from wx.lib.mixins.listctrl import ListCtrlAutoWidthMixin

actresses = [('jessica alba', 'pomona', '1981', '2'),
             ('sigourney weaver', 'new york', '1949', '3'),
             ('angelina jolie', 'los angeles', '1975', '4'),
             ('natalie portman', 'jerusalem', '1981', '5'),
             ('rachel weiss', 'london', '1971', '6'),
             ('scarlett johansson', 'new york', '1984', '7')]


class AutoWidthListCtrl(wx.ListCtrl, ListCtrlAutoWidthMixin):
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, -1, style=wx.LC_REPORT)
        ListCtrlAutoWidthMixin.__init__(self)


class Actresses(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(580, 330))

        hbox = wx.BoxSizer(wx.HORIZONTAL)

        panel = wx.Panel(self, -1)

        self.list = AutoWidthListCtrl(panel)
        self.list.InsertColumn(0, '名字', width=200)
        self.list.InsertColumn(1, '地点', width=150)
        self.list.InsertColumn(2, '年份', wx.LIST_FORMAT_CENTER, width=120)
        self.list.InsertColumn(3, '其他', wx.LIST_FORMAT_RIGHT, width=100)

        for i in actresses:
            index = self.list.InsertItem(sys.maxint, "\t\t" + i[0])
            self.list.SetItem(index, 1, i[1])
            self.list.SetItem(index, 2, i[2])
            self.list.SetItem(index, 3, i[3])

        hbox.Add(self.list, 1, wx.EXPAND)
        panel.SetSizer(hbox)

        self.Centre()
        self.Show(True)


app = wx.App()
Actresses(None, -1, '列表显示')
app.MainLoop()
