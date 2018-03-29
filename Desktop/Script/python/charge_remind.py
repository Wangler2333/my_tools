#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import time
import commands

target_level = 30
picture = "/Library/Scripts/MyScript/picture/battery_check.jpg"

'''
提供参数：
  1. 希望提醒的电量值
  2. 打开图片的路径

  新更改： 检查电量，达到标准设定值后会进行图片提示以及语音提示，无限循环，只有当插上电源后会自动停止。
          下次开始检测是在插上电源后600s (无限循环)
'''


def check_battery():
    try:
        current_capacity = commands.getoutput(
            "system_profiler SPPowerDataType | grep \"Charge Remaining\" | sed 's/.*: //'")
        full_capacity = commands.getoutput(
            "system_profiler SPPowerDataType | grep \"Full Charge Capacity\" | sed 's/.*: //' ")
        current_level = int((float(current_capacity) / float(full_capacity)) * 100)
        return current_level
    except:
        pass


def adaptor_check():
    try:
        present_check = commands.getoutput("system_profiler SPPowerDataType | grep \"Connected:\" | sed 's/.*: //'")
        if str(present_check) == "Yes":
            return 1
        else:
            return 0
    except:
        pass


def cylce_check(target_level):
    try:
        quit_check = 0

        while True:

            battery_level = check_battery()

            print "当前电量为: " + str(battery_level) + '%'
            time.sleep(3)

            if int(battery_level) <= target_level:

                while True:
                    os.system("open %s" % picture)
                    os.system("say 该充电了")
                    time.sleep(2)

                    if int(adaptor_check()) == 1:
                        quit_check = 1
                        os.system('killall -m Preview')

                    if quit_check == 1:
                        break

            if quit_check == 1:
                break
    except:
        pass


if __name__ == '__main__':
    while True:
        cylce_check(target_level)
        time.sleep(600)
