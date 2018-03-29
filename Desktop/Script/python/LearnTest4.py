#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import dns.resolver
import os
import httplib
import urllib2,urllib
import difflib

iplist = []
appdomain = "apple.com"

def get_iplist(domain=""):
    try:
        A = dns.resolver.query(domain, 'A')
    except Exception,e:
        print "dns resolver error: " + str(e)
        return
    for i in A.response.answer:
        for j in i.items:
            iplist.append(j.address)
    return True

def checkip(ip):
    checkurl = ip + ":80"
    getcontent = ""
    httplib.socket.setdefaulttimeout(5)
    conn = httplib.HTTPConnection(checkurl)

    try:
        result = urllib2.Request(checkurl)
        print result
        RESULT = urllib2.urlopen(result).read()
        conn.request("GET", "/", headers = {"Host": appdomain})

        r = conn.getresponse()
        getcontent = r.read(15)
        print RESULT
    finally:
        if getcontent == "<!doctype html>":
            print ip + " [OK}"
        else:
            print ip + " [Error]"

if __name__ == "__main__":
    if get_iplist(appdomain) and len(iplist) > 0:
        for ip in iplist:
            checkip(ip)
    else:
        print "dns resolver error. "
