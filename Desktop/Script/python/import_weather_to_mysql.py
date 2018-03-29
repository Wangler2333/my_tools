#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import csv
import smtplib
import collections
from email.mime.text import MIMEText
from email.utils import formataddr


'''
n = 0

with open('/Users/sasenyzhou/Documents/Weather/weather_get.csv') as f_obj:
    csv_reader = csv.reader(f_obj)
    for row in csv_reader:
        n = n + 1
        if n != 1:
            print row[0],'\t', row[1],'\t', row[2],'\t', row[3],'\t', row[4],'\t', row[5],'\t', row[6],'\t', \
            row[7],'\t', row[8],'\t', row[9],'\t', row[10],'\t', row[11],'\t', row[12], '\t', row[13]


#insert into Weather_Update (Crawl_time,City,Date,Update,Temperature,Weather,Wind,Humidity,Prompt,Pollute,Sun_up,Sun_down,Remind,After_24)

#insert into Weather_Update (Crawl_time,City,Date,Update,Temperature,Weather,Wind,Humidity,Prompt,Pollute,Sun_up,Sun_down,Remind,After_24) values ("07/29/2017_00:44:55","上海","2017-07-29 周六","00:30","30","多云","东风3级","湿度：71%","今天将现高温热浪，注意防暑|后天白天将出现大雨","28 | 优","05:08","18:53","穿衣: 薄短袖类 运动: 不适宜 感冒: 易发期 洗车: 不适宜","晴*晴*晴*晴*零散雷雨*零散 雷雨*零散雷雨*雷雨*零散雷雨*零散雷雨*局部多云*局部多云*少云*晴*晴*晴*晴*晴*晴*晴*晴*晴*晴*晴"
'''

#print dir(collections)


def mail():
    msg = MIMEText('邮件内容','plain','utf-8')
    msg['From'] = formataddr(["a","zuo0217@163.com"])
    msg['To'] = formataddr(["b","337418460@qq.com"])
    msg['Subject'] = "主题"

    server = smtplib.SMTP("smtp.163.com",25)
    server.login("zuo0217@163.com","411511656")
    server.sendmail('zuo0217@163.com',['337418460@qq.com',],msg.as_string())
    server.quit()

mail()
