#!/usr/bin/python

'test tcp client'

from socket import *
import threading

HOST = '127.0.0.1'
PORT = 21566
BUFSIZ = 1024
ADDR = (HOST, PORT)
threads = []


def Send(sock, test):  # 发送消息
    while True:
        data = input('>')
        tcpCliSock.send(data.encode('utf-8'))
        if data == 'quit':
            break


def Recv(sock, test):  # 接收消息
    while True:
        data = tcpCliSock.recv(BUFSIZ)
        if data == 'quit':
            sock.close()  # 退出时关闭socket
            break
        print(data)


tcpCliSock = socket(AF_INET, SOCK_STREAM)
tcpCliSock.connect(ADDR)

print('Please input your username:', )
username = input()
tcpCliSock.send(username.encode('utf-8'))
data = tcpCliSock.recv(BUFSIZ)
if data == 'Reuse':
    print('The username has been used!')
else:
    print('Welcome!')
    chat = threading.Thread(target=Send, args=(tcpCliSock, None))  # 创建发送信息线程
    threads.append(chat)
    chat = threading.Thread(target=Recv, args=(tcpCliSock, None))  # 创建接收信息线程
    threads.append(chat)
    for i in range(len(threads)):  # 启动线程
        threads[i].start()
    threads[0].join()  # 在我们的设计中，send线程必然先于recv线程结束，所以此处只需要调用send的join，等待recv线程的结束。
