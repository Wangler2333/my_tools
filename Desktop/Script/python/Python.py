#!/usr/bin/env python

import wx
import sys
import os
import urllib2
import urllib
import matplotlib, random


'''
   For PDCA data scrap...
'''

def writefile(string,file):
    try:
        with open(file, 'a') as d:
            d.write(string + '\n')
    except IOError as i:
        print ('IOError:',i)

IP = "17.239.64.36"
Login = "Danny.Liu"
Password = "apple1234567890"
StartDate = "05/02/2017"
EndDate = "05/02/2017"
StartTime = "10:00"
EndTime = "20:00"

URL = 'http://17.239.64.36/cgi-bin/WebObjects/QCR.woa/6/wo/GKcPSLjaEWNAL9rKUtYtJg/121.5.1.1'

Line = ""

postdata = urllib.urlencode({
    'UserName': Login,
    'Password': Password
})

req = urllib2.Request(
        url=URL,
        data=postdata
    )

result = urllib2.urlopen(req).read()
resultpath = "/Users/saseny/Desktop/scrap/1234.txt"
writefile(result,resultpath)