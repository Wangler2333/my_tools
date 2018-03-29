#!/usr/bin/env python
# _*_ coding:utf8 _*_
import wx


class myapp(wx.App):
    def __init__(self, redirect):
        wx.App.__init__(self, redirect)
        pass

    def OnInit(self):
        frame = myframe(None, -1, 'my title')
        frame.Show()
        self.SetTopWindow(frame)
        return True


class myframe(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title)

        # 设置菜单
        menubar = wx.MenuBar()
        menu = wx.Menu()
        menubar.Append(menu, '文件')
        menu.Append(1, '文件')
        menu.Append(2, '设置')
        menu.Append(3, '退出')
        self.SetMenuBar(menubar)

        # 设置一个工具栏
        toolbar = self.CreateToolBar()
        toolbar.AddLabelTool(-1, '退出', wx.Bitmap('/Users/sasenyzhou/Desktop/123.png'))
        toolbar.Realize()
        self.Centre()

        # 设置一个状态栏
        statusbar = self.CreateStatusBar()
        statusbar.SetStatusText('哈哈')

        # 添加一个按钮事件
        panel = wx.Panel(self)
        button = wx.Button(panel, -1, '哈哈')
        self.Bind(wx.EVT_BUTTON, self.exitframe, button)
        pass

    def exitframe(self, event):
        self.Close()
        pass


if __name__ == '__main__':
    mainapp = myapp(redirect=False)
    mainapp.MainLoop()