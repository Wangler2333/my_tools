#!/usr/bin/env python
# -*- coding: UTF-8 -*-

'''
    - Create by Saseny on 2017/07/12
    - Created for PDCA scrapy data and download log;
    - This is a sample, so pls accept my apologies.
      PDCA 17.239.64.36
'''

import urllib
import urllib2
import re
import os
import shutil
import threading
import Queue
import time


def writefile(string, file):
    try:
        with open(file, 'a') as d:
            d.write(string + '\n')
    except IOError as i:
        print ('IOError:', i)


print "\033[1;32m" + '''
    1. 用于从PDCA上批量下载Log，首次使用需要输入PDCA IP、PDCA 账户和密码。
    2. 再次使用时，可以选择重新输入上述信息，也可以选择跳过上述输入，用原先存储的信息。
    3. 存储下载Log的路径文件夹，可以不输入， 不输入或者输入错误，
       会在 Downloads 目录下建立文件夹以脚本开始运行时间为文件名.
''' + "\033[0m"

q = Queue.Queue(0)
NUM_WORKERS = 10
mylock = threading.Lock()
Date = time.strftime("%Y_%m_%d_%H_%M_%S")

passwd_file = os.path.expanduser('~') + '/password.txt'

if os.path.isfile(passwd_file):
    delect_right = raw_input("是否删除账户信息文件重新输入(是输 1 ):")
    if delect_right == "1":
        os.system('rm -rf %s' % passwd_file)
        PDCAIPAdress = raw_input("请输入PDCA地址:")
        UserName = raw_input("请输入PDCA账号:")
        PassWord = raw_input("请输入PDCA账号密码:")
        writefile("IP:" + str(PDCAIPAdress), passwd_file)
        writefile("User:" + str(UserName), passwd_file)
        writefile("Password:" + str(PassWord), passwd_file)
    else:
        a = 0
        b = 0
        c = 0
        with open(passwd_file) as ap:
            for line in ap:
                if "IP:" in line:
                    ip = re.findall(r'\S*', line.split(':')[1])
                    if len(ip) > 0:
                        PDCAIPAdress = ip[0]
                        a = 1
                if "User:" in line:
                    us = re.findall(r'\S*', line.split(':')[1])
                    if len(us) > 0:
                        UserName = us[0]
                        b = 1
                if "Password:" in line:
                    pw = re.findall(r'\S*', line.split(':')[1])
                    if len(pw) > 0:
                        PassWord = pw[0]
                        c = 1
            if a != 1 or b != 1 or c != 1:
                print "请重新输入账户信息."
                os._exit(1)

else:
    os.system('rm -rf %s' % passwd_file)
    PDCAIPAdress = raw_input("请输入PDCA地址:")
    UserName = raw_input("请输入PDCA账号:")
    PassWord = raw_input("请输入PDCA账号密码:")
    writefile("IP:" + str(PDCAIPAdress), passwd_file)
    writefile("User:" + str(UserName), passwd_file)
    writefile("Password:" + str(PassWord), passwd_file)

formt = raw_input("请输入要下载的Log名字关键字:")
list_file = raw_input("请输入要下载Log的SN list文件路径:")
fpath = raw_input("请输入要存储下载Log的路径文件夹:")

logon_url = "http://%s/cgi-bin/WebObjects/QCR.woa/wa/logon" % PDCAIPAdress

if not os.path.isfile(list_file):
    print '\'' + str(list_file) + '\'' + " file not exist."
    os._exit(1)

if not os.path.isdir(fpath):
    print '\'' + str(fpath) + '\'' + " folder not exist."
    fpath = os.path.expanduser('~') + '/Downloads/' + Date
    os.system('mkdir -p %s' % fpath)
    print
    print "Use Logs Folder: " + str(fpath)
    print


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


def crawl_sitemap(serial_number):
    '''
    Encode User passwd and url for crawl
    :param serial_number: for serial number crawl
    :return: no return
    '''

    postdata = urllib.urlencode({
        'UserName': UserName,
        'Password': PassWord
    })

    url_for_use = urllib2.Request(
        url=logon_url,
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
            match = re.search(r'<a href="(.*?)">\s*?<span id = "product_history">Product History</span>', first_crawl)
            tmp_url = match.group(1)
            first_url = 'http://%s%s' % (PDCAIPAdress, tmp_url)
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
            match = re.search(r'<form name="f_7_1" method="post" action="(.*?)">(\s|.)*?<td>SN, PS, PO, or SO:</td>',
                              second_crawl)
            tmp_url = match.group(1)
            second_url = 'http://%s%s' % (PDCAIPAdress, tmp_url)
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
            third_crawl = urllib2.urlopen(url_for_use_two, timeout=30).read()
        except:
            continue

        if re.findall(r'<a target="PARENT" href="(.*?)">View process logs</a>', third_crawl):
            tmp_url_three = re.findall(r'<a target="PARENT" href="(.*?)">View process logs</a>', third_crawl)[0]
            third_url = 'http://%s%s' % (PDCAIPAdress, tmp_url_three)
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
            fourth_url = 'http://%s%s' % (PDCAIPAdress, tmp_url_four)
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

    mylock.release()
    logs_url = re.findall(
        r'<tr>\s*?<td.*?>\s*?<font.*?>(.*?)</font>\s*?</td>\s*?<td.*?>\s*?<font.*?>.*?</font>\s*?</td>\s*?<td.*?>\s*?<font.*?>(.*?)</font>\s*?</td>\s*?<td.*?>\s*?<font.*?> <a href="(.*?)" name=".*?"><img',
        last_crawl)
    if len(logs_url) > 0:
        for i in logs_url:
            uul = 'http://%s%s?7,7' % (PDCAIPAdress, i[2])
            if formt in i[0] and "CQA" not in i[0]:  ## 剔除 CQA Log
                r = urllib2.urlopen(urllib2.Request(uul))
                with open(fpath + '/' + i[0], 'wb') as f:
                    shutil.copyfileobj(r, f)


def doJob(job, worktype):
    mylock.acquire()
    print "> Starting  -- [" + str(job) + "]" + " --- Thread@ " + str(worktype)
    crawl_sitemap(job)
    print "> Finished  -- [" + str(job) + "]" + " --- Thread@ " + str(worktype)


def read_list(file):
    serial_number_list = []
    with open(file) as f_job:
        for line in f_job:
            sn = re.findall(r'C02[A-Z].{8}', line)
            if len(sn) > 0:
                serial_number_list.append(sn[0])

        return serial_number_list


if __name__ == '__main__':
    sn_list = read_list(list_file)
    print "Begin...."
    for i in sn_list:
        q.put(i)
    print "Job Qsize:", q.qsize()
    for x in range(NUM_WORKERS):
        MyThread(q, x).start()
