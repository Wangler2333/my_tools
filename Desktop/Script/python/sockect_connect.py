#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 10/30/17 10:35 AM
@author: Saseny Zhou
@File:   sockect_connect.py
"""

import socket
import time

address = ('127.0.0.1', 8000)

while True:
    sk = socket.socket()
    sk.connect(address)
    data = "yes"
    sk.send(bytes(data, 'utf-8'))
    a = sk.recv(1024)
    print(str(a, 'utf-8'))
    time.sleep(5)
    sk.close()
