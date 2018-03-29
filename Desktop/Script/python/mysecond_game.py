#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# -- >> 有道翻译


import urllib.request
import urllib.parse
import json
import os
import _thread


class translate(object):
    '''
       有道翻译，连接有道网络进行在线翻译.
    '''

    def __init__(self, content='你好!', times=10):
        self.url = 'http://fanyi.youdao.com/translate?smartresult = dict&smartresult = rule&smartresult = ugc&sessionFrom = http://www.youdao.com/'
        self.content = content
        self.retry_times = times
        self.date_read()
        self.head_read()

    def setContent(self):
        '''
           输入要进行翻译的内容.
        '''
        self.content = input("请输入需要翻译的内容:")

    def setRetryTime(self, times):
        '''
           设置 retry 次数.
        '''
        self.retry_times = times

    def date_read(self):
        '''
           提交表单内容.
        '''
        self.date = {
            'type': 'AUTO',
            'i': self.content,
            'doctype': 'json',
            'xmlVersion': '1.6',
            'keyfrom': 'fanyi.web',
            'ue': 'UTF-8',
            'typoResult': 'true'
        }

    def head_read(self):
        '''
           伪装浏览器连接.
        '''
        self.head = {
            'Referer': 'http://fanyi.youdao.com',
            'User-Agent': 'Paw/3.1.2 (Macintosh; OS X/10.12.2) GCDHTTPRequest'
        }

    def translation(self):
        '''
           网络翻译，连接次数默认为 10 次，可使用 setRetryTime 函数进行修改，或者类实例化的时候给定参数.
        '''
        for i in range(self.retry_times):
            if i == int(self.retry_times) - 1:
                print('连接网络失败!')
                os._exit(1)
            try:
                data = urllib.parse.urlencode(self.date).encode('utf-8')
                req = urllib.request.Request(self.url, data, self.head)
                response = urllib.request.urlopen(req)
                html = response.read().decode('utf-8')
            except:
                continue
            if html != None:
                break
        self.target = json.loads(html)
        self.print_result()

    def print_result(self):
        '''
           打印结果.
        '''
        _thread.start_new_thread(self.speak_out, ())
        print('\033[0;31m' + "翻译结果: \033[0;34m %s" % (self.target['translateResult'][0][0]['tgt']) + '\033[0;30m')

    def circulatory(self):
        '''
           无限循环，当输入为 q 时退出.
        '''
        while True:
            self.setContent()
            if self.content == 'q':
                break

            self.date_read()
            self.head_read()
            self.translation()

    def speak_out(self):
        '''
           读出翻译结果.
        '''
        try:
            os.system('say %s' % self.target['translateResult'][0][0]['tgt'])
        except:
            pass


t = translate(content='下雨了')
t.circulatory()
