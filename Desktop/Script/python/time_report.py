#!/usr/bin/env python
# -*- coding: UTF-8 -*-


import time
import os
import re

time_get = time.strftime("%Y-%m-%d_%H:%M:%S")


def speak_out(formt):
    try:
        os.system('say %s' % formt)
    except:
        pass


def date_time(formt):
    try:
        get_date = re.findall(r'\d{4}-\d{2}-\d{2}', formt)[0]
        get_time = re.findall(r'\d{2}:\d{2}:\d{2}', formt)[0]

        return get_date, get_time

    except:
        pass


if __name__ == '__main__':
    speak_out(time_get)
    print date_time(time_get)
