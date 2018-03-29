#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 10/30/17 10:27 AM
@author: Saseny Zhou
@File:   lesson_socket.py
"""

import socket
import datetime

ip = '172.22.145.178'

sk = socket.socket()
address = ('172.22.145.178', 8000)

sk.bind(address)

sk.listen(3)

print('waiting......')

while True:
    conn, addr = sk.accept()
    # data = input(">>> ")
    # conn.send(data.encode('utf-8'))  # bytes(data,'utf-8')
    # print(conn)
    # print(addr)
    data = conn.recv(1024)
    a = datetime.datetime.now()
    conn.send(bytes(a, 'utf-8'))

    print('waiting......')
