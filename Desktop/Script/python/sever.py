#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 10/30/17 1:47 PM
@author: Saseny Zhou
@File:   sever.py
"""

from socket import *
from time import *

HOST = '172.22.145.178'
PORT = 8000
BUFSIZ = 1024
ADDR = (HOST, PORT)

tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind(ADDR)
tcpSerSock.listen(5)

while True:
    print('waiting for connection ... ')
    tcpCliSock, addr = tcpSerSock.accept()
    print('connected from:', addr)

    while True:
        data = tcpCliSock.recv(BUFSIZ)
        print(str(data, 'utf-8'))
        mesg = input('>>> ')
        tcpCliSock.sendall(('[%s] %s' % (ctime(), mesg)).encode('utf-8'))
        if not data:
            break
    tcpCliSock.close()

tcpSerSock.close()
