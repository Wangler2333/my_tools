#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
import os
import random
#from my_tools import *

'''
def try_send_email(content, subject, from_email, to_email, passwd, from_name, to_name, use_server):
    for i in range(10):
        if i == 5:
            print "发送失败."
            os._exit(1)
        try:
            response = auto_send_mail(content, subject, from_email, to_email, passwd, from_name, to_name, use_server)
        except:
            continue
        if response == True:
            print "发送成功."
            break

def auto_send_mail(content, subject, from_email, to_email, passwd, from_name, to_name, use_server):
    result = True
    try:
        msg = MIMEText(content, 'plain', 'utf-8')
        msg['From'] = formataddr([from_name, from_email])
        msg['To'] = formataddr([to_name, to_email])
        msg['Subject'] = subject

        server = smtplib.SMTP(use_server, 25)
        server.login(from_email, passwd)
        server.sendmail(from_email, [to_email, ], msg.as_string())
        server.quit()

    except Exception:
        result = False

    return result


#try_send_email("你说什么呢", "测试", "zuo0217@163.com", "337418460@qq.com", "411511656", "Saseny", "zuozheng",
#                     "smtp.163.com")


print hash("/Users/sasenyzhou/PycharmProjects/PycharmProjects/APP/ForUse/file/wether1.csv")

#print chr(61)   #数字转成 ascii
#print ord('V')   #相反


a = random.randint(1,256)
print chr(a)


#compile(hash("/Users/sasenyzhou/PycharmProjects/PycharmProjects/APP/ForUse/file/wether1.csv"))
list = ['11','22','33']

for i, item in enumerate(list,1):print i,item

print pow(1,2,3)
'''


#os.stat()
print (123)

