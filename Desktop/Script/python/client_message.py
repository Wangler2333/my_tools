#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 10/30/17 3:24 PM
@author: Saseny Zhou
@File:   client_message.py
"""

import socket, select, string, sys


def prompt():
    sys.stdout.write('<You> ')
    sys.stdout.flush()


if __name__ == '__main__':
    # if (len(sys.argv) < 3):
    #    print('Usage: python chat_client.py hpstname port')
    #    sys.exit()

    HOST = '127.0.0.1'  # sys.argv[1]
    PORT = 9999  # int(sys.argv[2])

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)

    try:
        s.connect((HOST, PORT))
    except:
        print('Unable to connect')
        sys.exit()

    print('Connected to remote host. Start sending message')
    prompt()

    while 1:
        socket_list = [sys.stdin, s]
        read_sockets, write_sockets, error_sockets = select.select(socket_list, [], [])

        #print(read_sockets)
        #print(write_sockets)
        #print(error_sockets)

        for sock in read_sockets:
            if sock == s:
                data = sock.recv(4096)
                if not data:
                    print('\nDisconnected from chat server')
                    sys.exit()
                else:
                    sys.stdout.write(str(data, 'utf-8'))
                    prompt()
            else:
                msg = sys.stdin.readline()
                s.send(msg.encode('utf-8'))
                prompt()
