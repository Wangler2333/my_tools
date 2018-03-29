#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from my_tools import *

url = 'http://weather.sina.com.cn'
# 开始运行时间


# Html 文件临时存放路径
#html_tmp = os.path.expanduser('~') + '/Desktop/Get_File/' + str(time_start) + '.html'

# 检查临时文件夹是否存在
#if not os.path.isdir(os.path.expanduser('~') + '/Desktop/Get_File/'):
#    os.system('mkdir -p %s' % os.path.expanduser('~') + '/Desktop/Get_File/')

# 检查临时文件夹存放文件大小
#tmp_size = os.path.getsize(os.path.expanduser('~') + '/Desktop/Get_File/')
#if int(tmp_size) > 100000000:
#    os.system('rm -rf %s' % os.path.expanduser('~') + '/Desktop/Get_File/')

# 天气情况文件
weather_file = os.path.expanduser('~') + '/Documents/Weather/' + 'weather_get.csv'
future_weather_file = os.path.expanduser('~') + '/Documents/Weather/' + 'future_weather_get.csv'

# 检查天气情况文件是否存在
if not os.path.isfile(weather_file):
    title = "Crawl time" + ',' +  "City" + ',' + "Date" + ',' + "Update" + ',' + "Temp" + ',' + "Weather" + ',' + "Wind" + ',' \
            + "Humidity" + ',' + "Prompt" + ',' + "Pollute" + ',' + "Sun_Up" + ',' + "Sun_Down" + ',' + "Remind" + ',' + "After 24h"
    writefile(str(title),weather_file)
if not os.path.isfile(future_weather_file):
    title_future = ["爬取时间","日期","星期","白天","夜间","温度","风力","污染","程度"]
    write_csv(future_weather_file,title_future)


def process_future(html):
    try:
        future_weather = re.findall(r'<p .*?>(.*?)</p>\s*?<p .*?>(.*?)</p>\s*?<p .*?>\s*?.*?</p>\s*?<p .*?>\s*?<span .*?>(.*?)</span>.*?<span .*?>(.*?)</span>\s*?</p>\s*?<p .*?>(.*?)</p>\s*?<p .*?>(.*?)</p>\s*?<ul .*?>\s*?<li .*?>(.*?)</li>\s*?<li .*?>(.*?)</li>\s*?',html)

        if len(future_weather) > 0:
            for i in future_weather:
                list_result = []
                list_result.append(str(time_start))
                a,b,c,d,e,f,g,h = i
                list_result.append(str(a))
                list_result.append(str(b))
                list_result.append(str(c))
                list_result.append(str(d))
                list_result.append(str(e))
                list_result.append(str(f))
                list_result.append(str(g))
                list_result.append(str(h))
                writer = csv.writer(open(future_weather_file, 'a'))
                writer.writerow(list_result)
    except IOError as e:
        print ('IOError',e)

def process_current(html):

        current_city = re.findall(r'<h4 class="slider_ct_name" id = "slider_ct_name" >(.*?)</h4>', html)
        current_date = re.findall(r'<p class="slider_ct_date">(.*?)</p>', html)
        update_time = re.findall(r'<div.*?更新时间.*?>(.*?)</div>', html)
        current_pollute = re.findall(r'<div .*?>\s*?<h6>(.*?)</h6>\s*?<p>(.*?)</p>\s*?</div>\s*?<div.*?>\s*?<p.*?>(.*?)</p>', html)
        current_time_point = re.findall(r'<span class="blk3_starrise">(.*?)</span>\s*?<span class="blk3_starfall">(.*?)</span>', html)
        current_weather = re.findall(r'<div.*?>(.*?)&#8451;</div>\s*?<p.*?>\s*?(.*?)\&nbsp;\&nbsp;|\&nbsp;\&nbsp;\s*(\S*?)\&nbsp;\&nbsp;|\&nbsp;\&nbsp;(.*?)</p>\s*?</div>\s*?<div.*?>\s*?<span class=".*?" data-tipid="." data-tipcont="(.*?)">\s*?<span.*?></span>',html)
        after_temp = re.findall(r'data-temp="(.*?)"', html)
        after_weather = re.findall(r'data-tempname="(.*?)"', html)

        current_prompt = re.findall(r'<div .*?>\s*?<h4>(.*?)</h4>\s*?<p>(.*?)</p>\s*?</div>\s*?<div .*?>\s*?<h4>(.*?)</h4>\s*?<p>(.*?)</p>\s*?</div>\s*?<div .*?>\s*?<h4>(.*?)</h4>\s*?<p>(.*?)</p>\s*?</div>\s*?<div .*?>\s*?<h4>(.*?)</h4>\s*?<p>(.*?)</p>\s*?</div>',html)
        a,a1,b,b1,c,c1,d,d1 = current_prompt[0]

        e1 = str(a) + ': ' + str(a1)
        e2 =  str(b) + ': ' + str(b1)
        e3 =  str(c) + ': ' + str(c1)
        e4 = str(d) + ': ' + str(d1)

        eall = e1 + ' ' + e2 + ' ' + e3 + ' ' + e4

        city = current_city[0]
        date = current_date[0]
        update = update_time[0]

        # in real time
        return_list = []
        for i in current_weather:
            for j in i:
                h = re.findall(r'\S*',str(j).replace(' ',''))
                if h[0] != "":
                    return_list.append(str(h[0]))

        b1 = return_list[0]
        b2 = return_list[1]
        b3 = return_list[2]
        b4 = return_list[3]
        b5 = return_list[4]

        m,e,f = current_pollute[0]
        ef = str(e) + ' | ' + str(f)

        start,end = current_time_point[0]

        a = str(after_temp[0]).replace(',','*')
        d = str(after_weather[0]).replace(',','*')

        #c1,c2,c3,c4,c5,c6,c7,c8,c9,c10,c11,c12,c13,c14,c15,c16,c17,c18,c19,c20,c21,c22,c23 = after_temp[0]
        #d1,d2,d3,d4,d5,d6,d7,d8,d9,d10,d11,d12,d13,d14,d15,d16,d17,d18,d19,d20,d21,d22,d23,d24 = after_weather[0]

        result =  str(time_start) + ',' + str(city) + ',' + str(date) + ',' + str(update) + ',' + str(b1) + ',' + str(b2)\
                  + ',' + str(b3)  + ',' + str(b4)  + ',' + str(b5)  + ',' + str(ef)  + ',' + str(start) + ',' + str(end) + ',' + eall + ',' + d

        writefile(result,weather_file)



if __name__ == '__main__':
    n = 0
    while True:
        n = n + 1
        time_start = time.strftime("%m/%d/%Y_%H:%M:%S")
        html = get_crawl(url)
        #os.system('echo %s >> %s' % (str(html),os.path.expanduser('~') + '/Desktop/Get_File/' + str(time_start) + '.html'))
        process_future(html)
        process_current(html)
        print "The " + str(n) + " times."
        time.sleep(600)
