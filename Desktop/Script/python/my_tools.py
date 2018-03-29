# /usr/bin/env python
# -*- coding: UTF-8 -*-
# __author__: Saseny Zhou
# Created on 2017/07/28 witsh the first version
# Total Current Functions QTY:  2017/07/31    11
# Total Current Functions QTY:  2017/08/01    13


import mysql.connector
import urllib2
import re
import os
import csv
import time
import commands
import BeautifulSoup
import lxml

def connect_mysql(ip, user, password, port, DATEBASES):
    '''
    :param ip:               数据库IP:        '127.0.0.1'
    :param user:             数据库用户:       root
    :param password:         数据库账户密码:    ******
    :param port:             数据库接口:       3306
    :param DATEBASES:        数据库名称:       ForScript
    :return:                 返回数据库连接状态
    '''
    config = {
        'host': ip,
        'user': user,
        'password': password,
        'port': port,
        'database': DATEBASES,
        'charset': 'utf8'
    }
    try:
        cnn = mysql.connector.connect(**config)
        return cnn
    except mysql.connector.Error as a:
        print ('connect fails!{}'.format(a))


def writefile(string, file):
    '''
    :param string:     输出文本内容
    :param file:       输出文件路径
    :return:           无返回
    '''
    try:
        with open(file, 'a') as d:
            d.write(string + '\n')
    except IOError as i:
        print ('IOError:', i)


def get_crawl(url):
    '''
    :param url: 提供网络连接
    :return:    返回爬取得网页信息
    '''

    req = urllib2.Request(url)

    for i in range(6):

        if i == 5:
            print "-> 网页爬取失败,请检查网络连接."
            os._exit(1)

        try:
            response = urllib2.urlopen(req, timeout=30).read()

        except:
            continue

        if response != None:
            break

    return response


def write_csv(file_path, content_list):
    '''
    :param content_list:     输出文本内容
    :param file_path:        输出文件路径
    :return:                 无返回
    '''
    try:
        writer = csv.writer(open(file_path, 'a'))
        writer.writerow(content_list)
    except IOError as e:
        print ('IOError:', e)


def find_file(path, formet):
    '''
    :param path:        需要搜索的路径
    :param formet:      需要搜索的文件关键字
    :return:            返回匹配的文件路径
    '''
    try:
        a = []
        fns = [os.path.join(root, fn) for root, dirs, files in os.walk(path) for fn in files]
        for f in fns:
            if os.path.isfile(f):
                if formet in f:
                    a.append(f)
        return a
    except IOError as o:
        print ('IOError', o)


def Time_check(_time):
    '''
    :param _time:        输入时间格式: "%Y/%m/%d %H:%M:%S" or "%Y-%m-%d %H:%M:%S"
    :return:             返回时间戳
    '''
    try:
        formt_one = re.findall(r'\/', _time)
        formt_two = re.findall(r'\-', _time)
        if len(formt_one) > 0:
            a = 1
        if len(formt_two) > 0:
            a = 0
    except:
        print "格式不正常"
        os._exit(1)

    try:
        if a == 1:
            timeArray = time.strptime(_time, "%Y/%m/%d %H:%M:%S")
        if a == 0:
            timeArray = time.strptime(_time, "%Y-%m-%d %H:%M:%S")
        timeStamp = int(time.mktime(timeArray))
        return timeStamp
    except UnboundLocalError as p:
        print ('UnboundLocalError', p)


def speak_out(content):
    '''
    :param content: 提供要播报的内容
    :return:
    '''
    try:
        os.system('say %s' % content)
    except SystemError as e:
        print ('SystemError:', e)


def tar_file(file_path, format):
    '''
    :param file_path:   要解压的文件路径
    :param format:      要解压的文件类型      如: .tgz   .tar
    :return:
    '''
    try:
        filepath = os.path.dirname(file_path)
        os.system('cd %s ; tar -zxf %s &>/dev/null' % (filepath, file_path))
        folder_path = file_path.replace(format, '')
        return folder_path
    except TypeError as e:
        print ('TypeError:', e)


def current_time():
    '''
    :return: 返回当前时间     -- 格式: 2017_07_29_12_32_32
    '''
    try:
        return time.strftime("%Y_%m_%d_%H_%M_%S")
    except SystemError as e:
        print ('SystemError:', e)


def ip_check(cycle_time_set, usr_static_ip):
    '''
    :param cycle_time_set:        提供每次循环的时间间隔,得到结果 (Update time, Ip chenged(yes or no) ,ip list)
    :param usr_static_ip:         提供本机固定ip用于检测是否有IP变更
    :return:                      生成的结果存储在当前用户目录下

    Usage:   ip_check("10","172.22.145.137")     10: cycle_time / 172.22.145.137: static ip

    '''

    count = 0
    file_path = os.path.expanduser('~') + '/ip_list.csv'

    while True:

        if not os.path.isfile(file_path):
            a = "Update Time," + "Ip chenged," + "Ip list"
            writefile(str(a), file_path)

        if count == int(cycle_time_set):
            count = 0

        if count == 0:
            cmd = "ifconfig"
            date = time.strftime("%Y/%m/%d %H:%M:%S")
            write_list = []
            write_list.append(str(date))

            try:
                ifconfig = commands.getoutput(cmd)
                ip_info = re.findall(r'[0-9]*\.[0-9]*\.[0-9]*\.[0-9]*', ifconfig)

                if usr_static_ip in ip_info:
                    write_list.append("No")
                else:
                    write_list.append("Yes")
                r = write_list + ip_info
                writer = csv.writer(open(file_path, 'a'))
                writer.writerow(r)

            except SystemError as e:
                print ('SystemError:', e)

        count = count + 1
        time.sleep(1)


def get_weather(weather_file, future_weather_file):
    '''
    :param url:                        基于网址: http://weather.sina.com.cn
    :param weather_file:               天气文件输出路径
    :param future_weather_file:        未来天气文件输出路径
    :return:
    '''

    url = 'http://weather.sina.com.cn'
    html = get_crawl(url)
    time_start = time.strftime("%m/%d/%Y_%H:%M:%S")

    # 检查天气情况文件是否存在
    if not os.path.isfile(weather_file):
        title = "Crawl time" + ',' + "City" + ',' + "Date" + ',' + "Update" + ',' + "Temp" + ',' + "Weather" + ',' + "Wind" + ',' \
                + "Humidity" + ',' + "Prompt" + ',' + "Pollute" + ',' + "Sun_Up" + ',' + "Sun_Down" + ',' + "Remind" + ',' + "After 24h"
        writefile(str(title), weather_file)
    if not os.path.isfile(future_weather_file):
        title_future = ["爬取时间", "日期", "星期", "白天", "夜间", "温度", "风力", "污染", "程度"]
        write_csv(future_weather_file, title_future)

    # ---------------------------------------------------------------------------------------------------------------- #

    current_city = re.findall(r'<h4 class="slider_ct_name" id = "slider_ct_name" >(.*?)</h4>', html)
    current_date = re.findall(r'<p class="slider_ct_date">(.*?)</p>', html)
    update_time = re.findall(r'<div.*?更新时间.*?>(.*?)</div>', html)
    current_pollute = re.findall(
        r'<div .*?>\s*?<h6>(.*?)</h6>\s*?<p>(.*?)</p>\s*?</div>\s*?<div.*?>\s*?<p.*?>(.*?)</p>', html)
    current_time_point = re.findall(
        r'<span class="blk3_starrise">(.*?)</span>\s*?<span class="blk3_starfall">(.*?)</span>', html)
    current_weather = re.findall(
        r'<div.*?>(.*?)&#8451;</div>\s*?<p.*?>\s*?(.*?)\&nbsp;\&nbsp;|\&nbsp;\&nbsp;\s*(\S*?)\&nbsp;\&nbsp;|\&nbsp;\&nbsp;'
        r'(.*?)</p>\s*?</div>\s*?<div.*?>\s*?<span class=".*?" data-tipid="." data-tipcont="(.*?)">\s*?<span.*?></span>',
        html)
    after_temp = re.findall(r'data-temp="(.*?)"', html)
    after_weather = re.findall(r'data-tempname="(.*?)"', html)

    current_prompt = re.findall(
        r'<div .*?>\s*?<h4>(.*?)</h4>\s*?<p>(.*?)</p>\s*?</div>\s*?<div .*?>\s*?<h4>(.*?)</h4>\s*?<p>(.*?)</p>\s*?'
        r'</div>\s*?<div .*?>\s*?<h4>(.*?)</h4>\s*?<p>(.*?)</p>\s*?</div>\s*?<div .*?>\s*?<h4>(.*?)</h4>\s*?<p>(.*?)</p>\s*?</div>',
        html)
    a, a1, b, b1, c, c1, d, d1 = current_prompt[0]

    e1 = str(a) + ': ' + str(a1)
    e2 = str(b) + ': ' + str(b1)
    e3 = str(c) + ': ' + str(c1)
    e4 = str(d) + ': ' + str(d1)

    eall = e1 + ' ' + e2 + ' ' + e3 + ' ' + e4

    city = current_city[0]
    date = current_date[0]
    update = update_time[0]

    return_list = []
    for i in current_weather:
        for j in i:
            h = re.findall(r'\S*', str(j).replace(' ', ''))
            if h[0] != "":
                return_list.append(str(h[0]))

    b1 = return_list[0]
    b2 = return_list[1]
    b3 = return_list[2]
    b4 = return_list[3]
    b5 = return_list[4]

    m, e, f = current_pollute[0]
    ef = str(e) + ' | ' + str(f)

    start, end = current_time_point[0]

    a = str(after_temp[0]).replace(',', '*')
    d = str(after_weather[0]).replace(',', '*')

    result = str(time_start) + ',' + str(city) + ',' + str(date) + ',' + str(update) + ',' + str(b1) + ',' + str(b2) \
             + ',' + str(b3) + ',' + str(b4) + ',' + str(b5) + ',' + str(ef) + ',' + str(start) + ',' + str(
        end) + ',' + eall + ',' + d

    writefile(result, weather_file)

    # ---------------------------------------------------------------------------------------------------------------- #

    try:
        future_weather = re.findall(
            r'<p .*?>(.*?)</p>\s*?<p .*?>(.*?)</p>\s*?<p .*?>\s*?.*?</p>\s*?<p .*?>\s*?<span .*?>(.*?)</span>.*?<span .*?>(.*?)'
            r'</span>\s*?</p>\s*?<p .*?>(.*?)</p>\s*?<p .*?>(.*?)</p>\s*?<ul .*?>\s*?<li .*?>(.*?)</li>\s*?<li .*?>(.*?)</li>\s*?',
            html)

        if len(future_weather) > 0:
            for i in future_weather:
                list_result = []
                list_result.append(str(time_start))
                a, b, c, d, e, f, g, h = i
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
        print ('IOError', e)


def read_file(file):
    '''
    :param file:    提供要读取的文件路径
    :return:        返回文件行，以列表的格式返回
    '''
    return_list = []
    try:
        with open(file) as f_obj:
            for line in f_obj:
                return_list.append(str(line).replace('\n', ''))

            return return_list
    except TypeError as e:
        print ('TypeError:', e)


def read_csv(file, formt, key):
    '''
    :param file:    提供要读取的csv文件路径
    :param formt:   读取类型：Dic 和 normal 两种选择 key 是 Dic 里的列目录 | 如：read_csv("/Users/saseny/Desktop/Nvram/123.csv","Dic","Prompt"）Prompt是文件其中一个开头的名字
    :return:        返回读取list  | Dic： 返回文件首行，以及根据给定 key 返回当列 normal：返回双层列表格式的list
    '''
    if formt == "Dic":
        try:
            key_list = []
            csv_read = open(file, 'r')
            reader = csv.DictReader(csv_read)
            # print reader.fieldnames
            for i in reader:
                key_list.append(i[key])

            return reader.fieldnames, key_list

        except TypeError as e:
            print ('TypeError:', e)

    if formt == "normal":
        try:
            csv_read = open(file, 'r')
            reader = csv.reader(csv_read)

            count = 0
            return_list = []
            for row in reader:
                count = count + 1
                if count != 1:
                    return_list.append(row)
            return return_list
        except TypeError as e:
            print ('TypeError:', e)
