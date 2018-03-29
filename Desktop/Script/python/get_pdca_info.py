#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# __author__: Saseny Zhou


import urllib
import urllib2
import re
import os
import shutil
import plistlib
import sys
import time
import Queue
import threading
from bs4 import BeautifulSoup
from lxml import etree

info_list = {
    'PDCAIPAdress': '17.239.64.36',
    'UserName': 'Danny.Liu',
    'PassWord': 'apple1234567890',
    'formt': 'PRE_PASS',
    'fpath': ''
}

reload(sys)
sys.setdefaultencoding('utf-8')

default_info_file = os.path.dirname(sys.argv[0]) + '/default.plist'
if not os.path.isfile(default_info_file):
    plistlib.writePlist(info_list, default_info_file)

q = Queue.Queue(0)
NUM_WORKERS = 10
mylock = threading.Lock()


class MyThread(threading.Thread):
    def __init__(self, input, worktype):
        self._jobq = input
        self._work_type = worktype
        threading.Thread.__init__(self)

    def run(self):
        while True:
            if self._jobq.qsize() > 0:
                self._process_job(self._jobq.get(), self._work_type)
            else:
                break

    def _process_job(self, job, worktype):
        doJob(job, worktype)


class crawl_sitemap_get(object):
    def __init__(self, default_file):
        self.default_info_file = default_file
        self.default_file_check()
        self.Date = time.strftime("%Y_%m_%d_%H_%M_%S")
        self.fpath = os.path.expanduser('~') + '/Downloads/' + self.Date
        self.logon_url = "http://%s/cgi-bin/WebObjects/QCR.woa/wa/logon" % self.PDCAIPAdress

    def default_file_check(self):
        self.dict = plistlib.readPlist(self.default_info_file)
        self.PDCAIPAdress = self.dict['PDCAIPAdress']
        self.UserName = self.dict['UserName']
        self.PassWord = self.dict['PassWord']
        self.formt = self.dict['formt']

    def reSetfpath(self, newfpath):
        self.fpath = newfpath

    def write_file(self, string, file):
        try:
            with open(file, 'a') as d:
                d.write(string + '\n')
        except IOError as i:
            print ('IOError:', i)

    def mkdir_logsFolder(self):
        if not os.path.isdir(self.fpath):
            os.system('mkdir %s' % self.fpath)

    def only_download_logs(self, serial_number):

        postdata = urllib.urlencode({
            'UserName': self.UserName,
            'Password': self.PassWord
        })

        url_for_use = urllib2.Request(
            url=self.logon_url,
            data=postdata
        )

        for a in range(6):
            '''
               Set up x5 times for crawl, if all fail then exit.
               Crawl logon page.
            '''
            if a == 5:
                print "Logon QCR Fail."
                os._exit(1)
            try:
                first_crawl = urllib2.urlopen(url_for_use, timeout=10).read()
            except:
                continue

            if re.search(r'<form name=".*?" method="post" action="(.*?)">', first_crawl):
                match = re.search(r'<a href="(.*?)">\s*?<span id = "product_history">Product History</span>',
                                  first_crawl)
                tmp_url = match.group(1)
                first_url = 'http://%s%s' % (self.PDCAIPAdress, tmp_url)
                break

        for b in range(6):
            '''
               Set up x5 times for crawl, if all fail then exit.
               Redirect to product history page.
            '''
            if b == 5:
                print "FAIL redirect to product history page."
                os._exit(1)
            try:
                second_crawl = urllib2.urlopen(first_url, timeout=30).read()
            except:
                continue

            if re.search(r'<form name="f_7_1" method="post" action="(.*?)">(\s|.)*?<td>SN, PS, PO, or SO:</td>',
                         second_crawl):
                match = re.search(
                    r'<form name="f_7_1" method="post" action="(.*?)">(\s|.)*?<td>SN, PS, PO, or SO:</td>',
                    second_crawl)
                tmp_url = match.group(1)
                second_url = 'http://%s%s' % (self.PDCAIPAdress, tmp_url)
                break

        postdata = urllib.urlencode({
            '7.1.1': serial_number,
            '7.1.3': 'Search',
            '7.1.7': '0',
        })

        url_for_use_two = urllib2.Request(
            url=second_url,
            data=postdata
        )

        for c in range(6):
            if c == 5:
                print "%s -> ERROR, FAIL to search find this SN on PDCA" % (serial_number)
                os._exit(1)
            try:
                self.third_crawl = urllib2.urlopen(url_for_use_two, timeout=30).read()

            except:
                continue

            if re.findall(r'<a target="PARENT" href="(.*?)">View process logs</a>', self.third_crawl):
                tmp_url_three = re.findall(r'<a target="PARENT" href="(.*?)">View process logs</a>', self.third_crawl)[
                    0]
                third_url = 'http://%s%s' % (self.PDCAIPAdress, tmp_url_three)
                break

        for d in range(6):
            if d == 5:
                print "%s -> ERROR, FAIL to search find this SN Log on PDCA" % (serial_number)
                os._exit(1)
            try:
                fouth_crawl = urllib2.urlopen(third_url, timeout=30).read()

            except:
                continue

            if re.findall(r'<p><a href="(.*?)">Search all mounted process log servers</a></p>', fouth_crawl):
                tmp_url_four = \
                    re.findall(r'<p><a href="(.*?)">Search all mounted process log servers</a></p>', fouth_crawl)[0]
                fourth_url = 'http://%s%s' % (self.PDCAIPAdress, tmp_url_four)
                break

        for e in range(6):
            if e == 5:
                print "%s -> ERROR, The last page Fail." % (serial_number)
                os._exit(1)
            try:
                last_crawl = urllib2.urlopen(fourth_url, timeout=30).read()
            except:
                continue

            if re.search(r'<a href="(.*?)" name=".*?"><img', last_crawl):
                break
        logs_url = re.findall(
            r'<tr>\s*?<td.*?>\s*?<font.*?>(.*?)</font>\s*?</td>\s*?<td.*?>\s*?<font.*?>.*?</font>\s*?</td>\s*?<td.*?>\s*?'
            r'<font.*?>(.*?)</font>\s*?</td>\s*?<td.*?>\s*?<font.*?> <a href="(.*?)" name=".*?"><img',
            last_crawl)
        if len(logs_url) > 0:
            for i in logs_url:
                uul = 'http://%s%s?7,7' % (self.PDCAIPAdress, i[2])
                if self.formt in i[0] and "CQA" not in i[0]:  ## 剔除 CQA Log
                    r = urllib2.urlopen(urllib2.Request(uul))
                    with open(self.fpath + '/' + i[0], 'wb') as f:
                        shutil.copyfileobj(r, f)

    def read_page_info(self, serial_number):
        postdata = urllib.urlencode({
            'UserName': self.UserName,
            'Password': self.PassWord
        })

        url_for_use = urllib2.Request(
            url=self.logon_url,
            data=postdata
        )

        for a in range(6):
            '''
               Set up x5 times for crawl, if all fail then exit.
               Crawl logon page.
            '''
            if a == 5:
                print "Logon QCR Fail."
                os._exit(1)
            try:
                first_crawl = urllib2.urlopen(url_for_use, timeout=10).read()
            except:
                continue

            if re.search(r'<form name=".*?" method="post" action="(.*?)">', first_crawl):
                match = re.search(r'<a href="(.*?)">\s*?<span id = "product_history">Product History</span>',
                                  first_crawl)
                tmp_url = match.group(1)
                first_url = 'http://%s%s' % (self.PDCAIPAdress, tmp_url)
                break

        for b in range(6):
            '''
               Set up x5 times for crawl, if all fail then exit.
               Redirect to product history page.
            '''
            if b == 5:
                print "FAIL redirect to product history page."
                # frame.displayinfo(msg)
                os._exit(1)
            try:
                second_crawl = urllib2.urlopen(first_url, timeout=30).read()
            except:
                continue

            if re.search(r'<form name="f_7_1" method="post" action="(.*?)">(\s|.)*?<td>SN, PS, PO, or SO:</td>',
                         second_crawl):
                match = re.search(
                    r'<form name="f_7_1" method="post" action="(.*?)">(\s|.)*?<td>SN, PS, PO, or SO:</td>',
                    second_crawl)
                tmp_url = match.group(1)
                second_url = 'http://%s%s' % (self.PDCAIPAdress, tmp_url)
                break

        postdata = urllib.urlencode({
            '7.1.1': serial_number,
            '7.1.3': 'Search',
            '7.1.7': '0',
        })

        url_for_use_two = urllib2.Request(
            url=second_url,
            data=postdata
        )

        for c in range(6):
            if c == 5:
                print "%s -> ERROR, FAIL to search find this SN on PDCA" % (serial_number)
                os._exit(1)
            try:
                self.third_crawl = urllib2.urlopen(url_for_use_two, timeout=30).read()

            except:
                continue

            if re.findall(r'<a target="PARENT" href="(.*?)">View process logs</a>', self.third_crawl):
                tmp_url_three = re.findall(r'<a target="PARENT" href="(.*?)">View process logs</a>', self.third_crawl)[
                    0]
                third_url = 'http://%s%s' % (self.PDCAIPAdress, tmp_url_three)
                break

    def page_log_process(self, serial_number):
        self.only_download_logs(serial_number)
        self.write_file(self.third_crawl, self.fpath + '/' + serial_number + '.html')

    def page_info_process(self, serial_number):
        self.read_page_info(serial_number)
        #self.write_file(self.third_crawl, self.fpath + '/' + serial_number + '.html')

        #html = BeautifulSoup(self.third_crawl,"lxml")

        list = []

        page = etree.HTML(str(self.third_crawl).decode('utf-8'))
        hrefs = page.xpath(u"//font")
        for i in hrefs:
            if i.text != '\0' or i.text != '\n':
                #self.write_file(str(i.text).replace('\t', ''), self.fpath + '/' + serial_number + '.txt')
                list.append(i.text)

        print list


def read_txt(file):
    serial_number_list = []
    with open(file) as f_job:
        for line in f_job:
            sn = re.findall(r'C02[A-Z].{8}', line)
            if len(sn) > 0:
                serial_number_list.append(sn[0])

        return serial_number_list


def doJob(job, worktype):
    print 'download -> [%s]  - - @thread %s --> residue: [%i]' % (job, worktype, int(q.qsize()))
    # mylock.acquire()     # 加入线程锁
    #t.page_info_process(job)
    # mylock.release()     # 解除线程锁


def main(sn_list):
    t.reSetfpath('/Users/saseny/Downloads/Problem')  # 更改Log存储路径
    t.mkdir_logsFolder()  # 创建Log存储文件夹

    for i in sn_list:
        q.put(i)
    print "Job Qsize:", q.qsize()
    for x in range(NUM_WORKERS):
        MyThread(q, x).start()


if __name__ == '__main__':
    t = crawl_sitemap_get(default_info_file)

    #sn = read_txt('/Users/saseny/Desktop/ss.txt')
    sn = ['C02V617LHV2M']
    main(sn)
