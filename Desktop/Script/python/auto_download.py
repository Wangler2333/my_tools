#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time     : 2017/12/5下午12:53
# @Author   : Saseny Zhou
# @Site     : 
# @File     : auto_download.py
# @Software : PyCharm Community Edition


import pyautogui
import os
import time

app = '/Applications/Safari.app'

os.system('open -a %s' % app)


def find_location():
    time.sleep(5)
    print(pyautogui.position())


pyautogui.moveTo(800, 45)
time.sleep(1)
pyautogui.click()
pyautogui.typewrite('17.239.64.36')
pyautogui.press('return')
pyautogui.moveTo(603, 245)
time.sleep(1)
pyautogui.click()
pyautogui.moveTo(1148, 241)
time.sleep(1)
pyautogui.click()
pyautogui.typewrite('Saseny.Zhou')
time.sleep(1)
pyautogui.press('tab')
pyautogui.typewrite('zuozheng+123456')
time.sleep(1)
pyautogui.press('return')
pyautogui.moveTo(1145, 281)
pyautogui.click()
time.sleep(1)
pyautogui.moveTo(531, 372)
pyautogui.click()
time.sleep(1)
pyautogui.moveTo(374, 462)
pyautogui.click()
time.sleep(1)
pyautogui.typewrite('J79A')
time.sleep(1)
pyautogui.press('return')
pyautogui.press('tab')
time.sleep(1)
pyautogui.typewrite('2017/11/09')
pyautogui.press('return')
pyautogui.press('tab')
time.sleep(1)
pyautogui.typewrite('12:12:12')
pyautogui.press('return')
pyautogui.press('tab')
time.sleep(1)
pyautogui.typewrite('2017/12/04')
pyautogui.press('return')
pyautogui.press('tab')
time.sleep(1)
pyautogui.typewrite('12:12:12')
pyautogui.press('return')
pyautogui.moveTo(366, 612)
pyautogui.click()
time.sleep(1)
pyautogui.typewrite('WiFi BT OTA')
time.sleep(1)
pyautogui.press('return')
pyautogui.press('tab')
time.sleep(1)
pyautogui.typewrite('3AAwE78')
time.sleep(1)
pyautogui.press('return')


pyautogui.moveTo(257, 738)
#pyautogui.click()

find_location()


os.system('killall -m Safari')
