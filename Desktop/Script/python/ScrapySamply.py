#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import urllib2
import re
import urllib
import os
import time

URL = "http://17.239.64.36/cgi-bin/WebObjects/QCR.woa/wa/logon"
PDCAIPAdress = '17.239.64.36'
UserName = "Danny.Liu"
PassWord = "apple1234567890"

def crawl_sitemap(url,SN):
    postdata = urllib.urlencode({
        'UserName': UserName,
        'Password': PassWord
    })
    req = urllib2.Request(
        url=url,
        data=postdata
    )

    for i in range(10):
        if i > 6:
            print "Logon QCR Fail."
            os._exit(1)
        try:
            print "Logon PDCA, attempt %s" % (i)
            result1 = urllib2.urlopen(req, timeout=10).read()
        except:
            continue
        if re.search(r'<form name=".*?" method="post" action="(.*?)">', result1):
            print "PDCA logged on"
            # get product history page URL
            match = re.search(r'<a href="(.*?)">\s*?<span id = "product_history">Product History</span>', result1)
            tmp = match.group(1)
            UNITURL = 'http://%s%s' % (PDCAIPAdress,tmp)
            print UNITURL
            break

    for i in range(10):
        if (i > 5):
            print "FAIL redirect to product history page"
            os._exit(1)
        try:
            print "Redirect to product history page, attempt %s" % (i)
            result2 = urllib2.urlopen(UNITURL, timeout=30).read()
        except:
            continue
        if re.search(r'<form name="f_7_1" method="post" action="(.*?)">(\s|.)*?<td>SN, PS, PO, or SO:</td>', result2):
            print "Product history page logged on"

            # get the product history URL
            match = re.search(r'<form name="f_7_1" method="post" action="(.*?)">(\s|.)*?<td>SN, PS, PO, or SO:</td>',
                              result2)
            tmp = match.group(1)
            UNITURLx = 'http://%s%s' % (PDCAIPAdress, tmp)
            print UNITURLx
            break

    postdata = urllib.urlencode({
        '7.1.1': SN,
        '7.1.3': 'Search',
        '7.1.7': '0',
    })

    req1 = urllib2.Request(
        url=UNITURLx,
        data=postdata
    )

    for i in range(10):
        if (i > 5):
            print "%s -> ERROR, FAIL to search find this SN on PDCA" % (SN)
            os._exit(1)
        try:
            resultdo = urllib2.urlopen(req1, timeout=30).read()
            #print resultdo
            # OK, got to process log download
            print "%s -> query SN PDCA, attempt %s" % (SN, i)
        except:
            continue
        if re.findall(r'<a target="PARENT" href="(.*?)">View process logs</a>', resultdo):
            ure = re.findall(r'<a target="PARENT" href="(.*?)">View process logs</a>', resultdo)[0]
            UNITURLxt = 'http://%s%s' % (PDCAIPAdress, ure)
            print UNITURLxt
            break

    resultdoe = urllib2.urlopen(UNITURLxt, timeout=30).read()

    #print resultdoe

    if re.findall(r'<p><a href="(.*?)">Search all mounted process log servers</a></p>',resultdoe):
        uss = re.findall(r'<p><a href="(.*?)">Search all mounted process log servers</a></p>',resultdoe)[0]
        odjes = 'http://%s%s' % (PDCAIPAdress, uss)
        print odjes

        pdosjs = urllib2.urlopen(odjes, timeout=30).read()

        #print pdosjs



'''
    if resultdo:
        Description = re.findall(r'<b>Description:</b>\s*?</font>\s*?</td>\s*?<td>\s*?<font size = "2">(.*?)</font>',resultdo)
        ANTENNA_VENDOR = re.findall(r'<font size = "2">ANTENNA_VENDOR</font>\s*?</td>\s*?<td align = ".*" width = ".*?">\s*?<font size = "2">(.*?)</font>',resultdo)
        Configurable = re.findall(r'<font size = "2">Configurable Options:</font>\s*?</b>\s*?</td>\s*?<td>\s*?<font size = "2">(.*?)</font>',resultdo)
        MPN_SO = re.findall(r'<b>MPN/SO#:</b>\s*?</font>\s*?</td>\s*?<td>\s*?<table .*?>\s*?<tr .*?>\s*?<td>\s*?<font size = "2">(.*?)</font>',resultdo)

        if len(Description) == 1 and len(ANTENNA_VENDOR) == 1 and len(Configurable) and len(MPN_SO) == 1:
            WIP = str(SN) + '+' + str(MPN_SO[0])
            reded = SN + ',' + str(MPN_SO[0]) + ',' + WIP + ',' + str(ANTENNA_VENDOR[0]) + ',' + str(Description[0]) + ',' + str(Configurable[0].replace(',','/'))
            writefile(reded,Resultpath)

def SnList(path):
    SNList = []
    with open(path) as f:
        for line in f:
            a = line.rsplit()[0]
            if len(a) == 12:
                SNList.append(a)
        return SNList

def writefile(string,file):
    try:
        with open(file, 'a') as d:
            d.write(string + '\n')
    except IOError as i:
        print ('IOError:',i)

def Process():
    Path = e.get()
    if not os.path.isfile(Resultpath):
        red = "Serial Number" + ',' + "Model Number" + ',' + "WIP" + ',' + "Antenna Vendor" + ',' + "Description" + ',' + "Configurable"
        writefile(red, Resultpath)
    SNList = SnList(Path)
    for sn in SNList:
        crawl_sitemap(URL, sn)
'''

if __name__ == '__main__':
    crawl_sitemap(URL,'C02V13GAHV2M')
    #Date = time.strftime("%Y_%m_%d_%H_%M_%S")
    #Resultpath = os.path.expanduser('~') + "/Desktop/" + Date + '.csv'
    #result = os.path.dirname(Resultpath)

