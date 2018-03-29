#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import psutil
import datetime
from subprocess import Popen, PIPE
import IPy

def function(a, b):
    print a,b

apply(function,("whither","canada"))
apply(function,(1,2 + 3))
apply(function,("crunchy",{"b": "frog"}))
apply(function,((),{"a":"crunchy","b": "frog"}))

print psutil.virtual_memory().free                 # 剩余空间
print psutil.cpu_times()                           # 获取CPU完整信息，需要显示所有逻辑CPU信息
print psutil.cpu_count()                           # 获取CPU逻辑个数，默认 logical=True4
print psutil.cpu_count(logical=False)              # 获取CUP的物理个数
print psutil.disk_partitions()                     # 获取磁盘完整信息
print psutil.disk_usage('/')                       # 获取分区（参数）的使用情况
print psutil.disk_io_counters()                    # 获取硬盘总的IO个数、读写信息
print psutil.disk_io_counters(perdisk=False)       # 获取单个分区IO个数、读写信息
print psutil.net_io_counters()                     # 获取网络总的IO信息，默认 pernic=False
print psutil.net_io_counters(pernic=True)          # 输出每个网络接口的IO信息

print psutil.users()                               # 返回当前登陆系统的用户信息
print psutil.boot_time()                           # 获取开机时间，以Linux时间戳格式返回  ⬇️ 通过datetime进行时间格式转换
print datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")

print psutil.pids()                                # 列出所有进程 PID
p = psutil.Process(233)                            # 实例化一个Process对象，参数为一进程PID
print p.name()                                     # 进程名
print p.exe()                                      # 进程 bin 路径
print p.status()                                   # 进程状态
print p.uids()                                     # 进程 uid 信息
print p.gids()                                     # 进程 gid 信息
#print p.cpu_times()                                # 进程CPU时间信息，包括user、system两个CPU时间
#print p.cpu_affinity()                             # get 进程CPU亲和度，如果要设置进程CPU亲和度，将CPU号作为参数即可
#print p.memory_percent()                           # 进程内存利用率
#print p.memory_info()                              # 进程内存 rss、vms信息
#print p.io_counters()                              # 进程IO信息，包括读写IO数及字节数
#print p.connections()                              # 返回打开进程socket的namedutples列表，包括fs、family、laddr等信息
#print p.num_threads()                              # 进程开启的线程数

d = psutil.Popen(["/usr/bin/python", "-c", "print ('hello')"], stdout=PIPE)           # 通过psutil的Popen方法启动的应用程序，可以跟踪该程序运行的所有相关信息
print d
print d.name()
print d.username()
print d.communicate()[0]
#print d.cpu_times()

print Popen(["/usr/sbin/diskutil","list"],stdout=PIPE).communicate()[0]

'''
************** IPy model *************
'''

print IPy.IP('10.0.0.0/8').version()
print IPy.IP('::1').version()
print IPy.IP('192.168.1.0').version()

ip = IPy.IP('192.168.0.0/16')
print ip.len()
print len(ip)

#for x in ip:
   # print x

