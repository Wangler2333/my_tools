#!/usr/bin/env python
#coding=utf-8

import urllib2,urllib
import re, cookielib
import os, sys

def writefile(string,file):
    try:
        with open(file, 'a') as d:
            d.write(string + '\n')
    except IOError as i:
        print ('IOError:',i)

PDCAIPAdress="17.239.64.36"
URL="http://%s/cgi-bin/WebObjects/QCR.woa/wa/logon"%(PDCAIPAdress)

#f = urllib2.urlopen(URL).read()


def logonPDCAQCR():
    # Enable cookie
    global URL
    global UNITURL

    cookie_support = urllib2.HTTPCookieProcessor(cookielib.CookieJar())
    opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
    urllib2.install_opener(opener)
    # login in to QCR first

    postdata = urllib.urlencode({
        'UserName': "Danny.Liu",
        'Password': "apple1234567890"
    })
    #
    req = urllib2.Request(
        url=URL,
        data=postdata
    )
    reudjsh = urllib2.urlopen(req).read()
    #print reudjsh
    resd = "http://%s/cgi-bin/WebObjects/QCR.woa/1/wo/VF3BM2HncwHVNJ0Whxh2Mw/0.3"%PDCAIPAdress
    rewd = urllib2.Request(url=resd,data=postdata)
    #print urllib2.urlopen(rewd).read()

    # try to logon PDCA first
    for i in range(10):
        if (i > 5):
            print "FAIL to logon PDCA"
            os._exit(1)
        try:
            print "Logon PDCA, attempt %s" % (i)
            result = urllib2.urlopen(req, timeout=10).read()
        except:
            continue
        if re.search(r'<form name=".*?" method="post" action="(.*?)">', result):
            print "PDCA logged on"
            # get product history page URL
            match = re.search(r'<a href="(.*?)">\s*?<span id = "product_history">Product History</span>', result)
            tmp = match.group(1)
            UNITURL = 'http://%s%s' % (PDCAIPAdress, tmp)
            URLd = 'http://17.239.64.36/cgi-bin/WebObjects/QCR.woa/6/wo/9oizD1wz1cYV972clSdaYw/70.7.1.1.1.1.45.41.1.1.1.3.1.0.1.0#MYCOLLAPSIBLECOMP19562'
            req2 = urllib2.Request(
                url=URLd,
                data=postdata
            )
            reudjsh1 = urllib2.urlopen(req2).read()
            print reudjsh1
            writefile(reudjsh1,"/Users/saseny/Desktop/resjk.txt")

            break

    # click product history, so that we can query both FATP and module
    for i in range(10):
        if (i > 5):
            print "FAIL redirect to product history page"
            os._exit(1)
        try:
            print "Redirect to product history page, attempt %s" % (i)
            result = urllib2.urlopen(UNITURL, timeout=30).read()
        except:
            continue
        if re.search(r'<form name="f_7_1" method="post" action="(.*?)">(\s|.)*?<td>SN, PS, PO, or SO:</td>', result):
            print "Product history page logged on"

            # get the product history URL
            match = re.search(r'<form name="f_7_1" method="post" action="(.*?)">(\s|.)*?<td>SN, PS, PO, or SO:</td>',
                              result)
            tmp = match.group(1)
            UNITURL = 'http://%s%s' % (PDCAIPAdress, tmp)
            break
    # print UNITURL
    # OK, now we have logged in QCR and let's go to systerm yield
    sys.stdout.flush()
    #print result

#writefile(f,"/Users/saseny/Desktop/resjk.txt")
logonPDCAQCR()





#mes = re.findall(r'<a href="(.*?)">QCR</a><br>',f)

#print mes

