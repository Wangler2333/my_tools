#!/usr/bin/env python

import wx
import images    

class App(wx.App):

    def __init__(self, redirect=True, filename=None):
        wx.App.__init__(self, redirect, filename)
    
    def OnInit(self):
        dlg = wx.MessageDialog(None, 'Is this the coolest thing ever!',
                          'MessageDialog', wx.YES_NO | wx.ICON_QUESTION)
        result = dlg.ShowModal()
        print result
        print wx.ID_YES
        print wx.ID_NO
        
        dlg.Destroy()

        dlg1 = wx.TextEntryDialog(None, "Who is buried in Grant's tomb?",
                'A Question', 'Cary Grant')
        if dlg1.ShowModal() == wx.ID_OK:
            response = dlg1.GetValue()
        dlg1.Destroy()

        dlg2 = wx.SingleChoiceDialog(None, 
                'What version of Python are you using?', 'Single Choice',
               ['1.5.2', '2.0', '2.1.3', '2.2', '2.3.1'])
        if dlg2.ShowModal() == wx.ID_OK:
            response = dlg2.GetStringSelection()
        dlg2.Destroy()

        return True


if __name__ == '__main__':
    app = App()
    fred = app.MainLoop()
    
