#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import pandas as pd
import xlrd
import xlwt
import encodings
import commands

from check_weather import process_info
import scrapy



codeCodes = {
    '黑色': '0;30',
    'bright gray': '0;37',
    '蓝色': '0;34',
    '白色': '1;37',
    '绿色': '0;32',
    'bright blue': '1;34',
    'cyan': '0;36',
    'bright green': '1;32',
    '红色': '0;31',
    'bright cyan': '1;36',
    'purple': '0;35',
    'bright red': '1;31',
    '***': '0;30',
    'bright purple': '1;35',
    '灰色': '1;30',
    'bright yellow': '1;33',
    '正常': '0'
}

def f(text,color):
    return "\033[" + color + "m" + text + "\t" + text + "\t" + text + "\033[0m"




for x in codeCodes:
    print f(str(x),codeCodes[x])


weather_url = 'http://www.weather.com.cn/weather1d/101020100.shtml#search'
process_info(weather_url)