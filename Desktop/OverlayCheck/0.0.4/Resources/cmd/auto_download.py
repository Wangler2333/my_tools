#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time     : 2017/12/11下午12:03
# @Author   : Saseny Zhou
# @Site     : 
# @File     : auto_download.py
# @Software : PyCharm Community Edition


import pyautogui
import os, sys
import time
import biplist

base_dir = os.path.dirname(sys.argv[0])
config_path = os.path.join(base_dir, 'config.plist')


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


def main(download):
    config_info = download
    location = config_info['request']['my_location']
    user_info = config_info['info']
    t = AutoDownload(config_info['app'], config_info['delay'])
    t.open()
    t.move(location['new_window'])
    t.move(location['create'])
    t.move(location['ip_input'])
    t.write(user_info['ip'])
    t.enter()
    t.move(location['user_input'])
    pyautogui.click()
    t.move(location['username'])
    t.write(user_info['username'])
    t.tab()
    t.write(user_info['password'])
    t.move(location['login'])
    t.move(location['report'])
    pyautogui.moveTo(location['restore report'])
    t.move(location['default'])
    t.move(location['download'])
    time.sleep(user_info['quit delay'])
    t.close()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == '-p':
            time.sleep(3)
            print(pyautogui.position())
            sys.exit(0)
        if sys.argv[1] == '-d':
            try:
                main(biplist.readPlist(sys.argv[2]))
            except IOError as e:
                print('Error, Pls check')
