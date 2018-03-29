#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# -*- coding: GBK -*-

import smtplib
import string

HOST = "smtp.quantacn.com"
SUBJECT = "Test email from Python."
TO = "brant.zhen@quantacn.com"
FROM = "saseny.zhou@quantacn.com"
text = "Python rules them all!"
BODY = string.join((
    "From: %s" % FROM,
    "To: %s" % TO,
    "Subject: %s" % SUBJECT,
    "",
    text
), "\r\n")

server = smtplib.SMTP()
server.connect(HOST,"25")
server.starttls()
server.login("saseny.zhou@quantacn.com","zuozheng@123456")
server.sendmail(FROM,[TO],BODY)
server.quit()