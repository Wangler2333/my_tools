#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time     : 2017/12/5下午12:48
# @Author   : Saseny Zhou
# @Site     :
# @File     : auto_download.py
# @Software : PyCharm Community Edition

import pyautogui
import os, sys
import time
import plistlib


class AutoDownload(object):
    def __init__(self, app, delay):
        self.app = app
        self.delay = delay

    def open(self):
        os.system('open -a %s' % self.app)

    def close(self):
        os.system('killall -m %s' % os.path.basename(self.app).replace('.app', ''))

    def move(self, args):
        pyautogui.moveTo(int(args[0]), int(args[1]))
        time.sleep(self.delay)
        pyautogui.click()

    def write(self, string):
        pyautogui.typewrite(str(string))
        time.sleep(self.delay)

    def tab(self):
        pyautogui.press('tab')

    def enter(self):
        pyautogui.press('return')

    def double(self, x, y):
        time.sleep(2)
        for i in xrange(10):
            y += 5
            pyautogui.moveTo(x, y)
            pyautogui.click()
            time.sleep(2)


def request(args):
    t = AutoDownload(args['app'], args['delay'])

    location = args['request']['my_location']
    user_info = args['info']
    download_info = args['define']

    t.open()
    t.move(location['new_window'])
    t.move(location['create'])
    t.move(location['ip_input'])
    t.write(user_info['ip'])
    t.enter()
    t.move(location['QCR_location'])
    t.move(location['user_input'])
    t.write(user_info['user'])
    t.tab()
    t.write(user_info['password'])
    t.enter()
    t.move(location['PFA_location'])
    t.move(location['P-Data'])
    t.move(location['Product'])
    t.write(download_info['product'])
    t.enter()
    t.tab()
    t.write(download_info['start date'])
    t.enter()
    t.tab()
    t.write(download_info['start time'])
    t.enter()
    t.tab()
    t.write(download_info['end data'])
    t.enter()
    t.tab()
    t.write(download_info['end time'])
    t.enter()
    t.tab()
    t.move(location['Station'])
    t.write(download_info['station'])
    t.enter()
    t.tab()
    t.write(download_info['overlay'])
    t.enter()
    t.double(location['Submit'][0], location['Submit'][1])
    time.sleep(args['request']['delay'])
    t.close()


def download(args):
    t = AutoDownload(args['app'], args['delay'])
    location = args['download']['my_location']
    user_info = args['info']
    t.open()
    t.move(location['new_window'])
    t.move(location['create'])
    t.move(location['ip_input'])
    t.write(user_info['ip'])
    t.enter()
    t.move(location['QCR_location'])
    t.move(location['user_input'])
    t.write(user_info['user'])
    t.tab()
    t.write(user_info['password'])
    t.enter()
    t.move(location['PFA_location'])
    t.move(location['manage Tasks'])
    t.move(location['download'])
    time.sleep(args['download']['delay'])
    t.close()


def delete(args):
    t = AutoDownload(args['app'], args['delay'])
    location = args['delete']['my_location']
    user_info = args['info']
    t.open()
    t.move(location['new_window'])
    t.move(location['create'])
    t.move(location['ip_input'])
    t.write(user_info['ip'])
    t.enter()
    t.move(location['QCR_location'])
    t.move(location['user_input'])
    t.write(user_info['user'])
    t.tab()
    t.write(user_info['password'])
    t.enter()
    t.move(location['PFA_location'])
    t.move(location['manage Tasks'])
    t.move(location['delete'])
    t.move(location['confirm'])
    time.sleep(args['delete']['delay'])
    t.close()


def read_plist(file_path):
    try:
        return plistlib.readPlist(file_path)
    except TypeError as e:
        print 'File Error', e
        sys.exit(1)


def main(args):
    if len(args) == 3 and str(args[2]).endswith('.plist'):
        if args[1] == '-request':
            request(read_plist(args[2]))
        if args[1] == '-download':
            download(read_plist(args[2]))
        if args[1] == '-delete':
            delete(read_plist(args[2]))
        if args[1] in ['-h', '--help']:
            print """
            Usage:
                       <cmd> -request config_file    -- Data Request
                       <cmd> -download config_file   -- Data Download
                       <cmd> -delete config_file     -- Delete request record
            """


if __name__ == "__main__":
    main(sys.argv)
