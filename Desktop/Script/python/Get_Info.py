#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import urllib
import urllib2
import re

unit = '℃'

# url = 'http://www.weather.com.cn/weather/101010100.shtml'
url = 'http://www.weather.com.cn/weather1d/101020100.shtml#search'

req = urllib2.Request(url)
response = urllib2.urlopen(req).read()

result_ = re.findall(r'<script>\s*?var hour3data={(.*?)}\s*?</script>', response)

now = re.findall(
    r'<div class="sk">\s*?</div>\s*?<ul.*?>\s*?<li>\s*?<h1>(.*?)</h1>\s*?<big.*?></big>\s*?'
    r'<p.*?>(.*?)</p>\s*?<div.*?>\s*?</div>\s*?<p.*?>\s*?<span>(.*?)</span><em>(.*?)</em>\s*?</p>\s*?<p.*?">\s*?'
    r'<i.*?></i>\s*?<span.*?>(.*?)</span>\s*?</p>\s*?<p.*?><i></i>\s*?<span>(.*?)</span>',
    response)

result = str(result_).replace('[', '').replace(']', '').split('"')

print now[0]

time_now, weather, temperature, unit_none, wind, sunset = now[0]

print time_now.decode('string_escape').decode("utf-8"), weather.decode('string_escape').decode("utf-8"), str(
    temperature.decode('string_escape').decode("utf-8")) + str(unit), wind.decode('string_escape').decode(
    "utf-8"), sunset.decode('string_escape').decode("utf-8")

# ssd = str(result).decode('string_escape').decode("utf-8")

for i in result:
    if str(i) != ',' and str(i) != '\'' and str(i) != ':':
        print str(i).decode('string_escape').decode("utf-8")
