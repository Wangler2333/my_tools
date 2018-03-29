# /usr/bin/env python
# -*- coding: UTF-8 -*-


import my_tools
import re
import time
import os

if not os.path.isdir(os.path.expanduser('~') + '/Desktop/Get_File/'):
    os.system('mkdir -p %s' % os.path.expanduser('~') + '/Desktop/Get_File/')

time_start = time.strftime("%s")
print time_start

url = 'http://news.baidu.com'
url1 = 'http://www.sina.com.cn'
url2 = 'http://weather.sina.com.cn'

html = my_tools.get_crawl(url2)
print time.strftime("%s")

my_tools.writefile(str(html), os.path.expanduser('~') + '/Desktop/Get_File/' + str(time_start) + '.html')

#  1
city = re.findall(r'<h4 class="slider_ct_name" id = "slider_ct_name" >(.*?)</h4>', html)
print str(city).decode('string_escape').decode("utf-8")

#  2
date = re.findall(r'<p class="slider_ct_date">(.*?)</p>', html)
print str(date).decode('string_escape').decode("utf-8")

#  3
update_time = re.findall(r'<div.*?更新时间.*?>(.*?)</div>', html)
print update_time

#  4
some = re.findall(
    r'<p .*?>(.*?)</p>\s*?<p .*?>(.*?)</p>\s*?<p .*?>\s*?.*?</p>\s*?<p .*?>\s*?<span .*?>(.*?)</span>.*?<span .*?>(.*?)'
    r'</span>\s*?</p>\s*?<p .*?>(.*?)</p>\s*?<p .*?>(.*?)</p>\s*?<ul .*?>\s*?<li .*?>(.*?)</li>\s*?<li .*?>(.*?)</li>\s*?',
    html)
print str(some).decode('string_escape').decode("utf-8")

#  5
futher_temp = re.findall(r'data-temp="(.*?)"', html)
print futher_temp

#  6
futher_weather = re.findall(r'data-tempname="(.*?)"', html)
print str(futher_weather).decode('string_escape').decode("utf-8")

#  7
futher = re.findall(
    r'<div.*?>(.*?)&#8451;</div>\s*?<p.*?>\s*?(.*?)\&nbsp;\&nbsp;|\&nbsp;\&nbsp;\s*(\S*?)\&nbsp;\&nbsp;|\&nbsp;\&nbsp;(.*?)</p>\s*?</div>\s*?<div.*?>\s*?<span class=".*?" data-tipid="." data-tipcont="(.*?)">\s*?<span.*?></span>',
html)
#print str(futher).decode('string_escape').decode("utf-8")

#  8
time_point = re.findall(r'<span class="blk3_starrise">(.*?)</span>\s*?<span class="blk3_starfall">(.*?)</span>', html)
print time_point

#  9
things = re.findall(
    r'<div .*?>\s*?<h4>(.*?)</h4>\s*?<p>(.*?)</p>\s*?</div>\s*?<div .*?>\s*?<h4>(.*?)</h4>\s*?<p>(.*?)</p>\s*?</div>\s*?<div .*?>\s*?<h4>(.*?)</h4>\s*?<p>(.*?)</p>\s*?</div>\s*?<div .*?>\s*?<h4>(.*?)</h4>\s*?<p>(.*?)</p>\s*?</div>',
    html)
print str(things).decode('string_escape').decode("utf-8")

# 10
pollution_standard_index = re.findall(
    r'<div .*?>\s*?<h6>(.*?)</h6>\s*?<p>(.*?)</p>\s*?</div>\s*?<div.*?>\s*?<p.*?>(.*?)</p>', html)
print str(pollution_standard_index).decode('string_escape').decode("utf-8")

return_list = []
for i in futher:
    for j in i:
        h = re.findall(r'\S*',str(j).replace(' ',''))
        if h[0] != "":
            return_list.append(str(h[0]))
print str(return_list).decode('string_escape').decode("utf-8")

print time.strftime("%s")
