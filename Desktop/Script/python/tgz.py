#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time     : 2017/11/17上午8:41
# @Author   : Saseny Zhou
# @Site     : 
# @File     : shell_tgz.py
# @Software : PyCharm Community Edition


import subprocess
import os
import sys
import time

message = '''Author:  Saseny
version: 0.0.1

Usage:
      cmd -c <obj> <True or Empty>  compress file to tgz file
      cmd -z <obj> <True or Empty>  uncompress file from tgz file
      if argv[3] is True then will remove source<obj> file
'''


def calculate(flag=False):
    def showtime(func):
        def inner(*args, **kwargs):
            strt_time = time.time()
            func(*args, **kwargs)
            end_time = time.time()
            print('Used Time: %s s' % (round(float(end_time) - float(strt_time), 2)))
            if flag:
                pass

        return inner

    return showtime


class FileProcess(object):
    '''
    Usage:
          for file compress and uncompress
          now only can use for tgz formt
    '''

    def __init__(self):
        self.compress = 'cd %s; tar -zcvf %s %s &>/dev/null'
        self.uncompress = 'cd %s; tar -xzf %s &>/dev/null'

    def shell(self, cmd):
        '''
        :param cmd:   input cmd and used shell command run it
        :return:      return run result and result code
        '''
        run = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        while run.poll() is None:
            pass
        return run.returncode, run.stdout.readlines()

    @calculate()
    def tgz_compress(self, obj, force=False):
        '''
        :param obj:     file path for compress
        :param force:   force to remove obj file when force is True
        :return:        no return
        '''
        path = os.path.dirname(obj)
        name = os.path.basename(obj)
        final = ".".join([name, "tgz"])
        a, b = self.shell(self.compress % (path, final, name))
        if force and a == 0:
            os.system('rm -rf %s' % obj)

    @calculate()
    def tgz_uncompress(self, obj, force=False):
        '''
        :param obj:     file path for uncompress
        :param force:   force to remove obj file when force is True
        :return:        no return
        '''
        path = os.path.dirname(obj)
        name = os.path.basename(obj)
        a, b = self.shell(self.uncompress % (path, name))
        if force and a == 0:
            os.system('rm -rf %s' % obj)


def check_input(args):
    if len(args) > 2:
        if '-c' in args:
            if os.path.isdir(args[2]) or os.path.isfile(args[2]):
                if 'True' in args:
                    t.tgz_compress(args[2], force=True)
                else:
                    t.tgz_compress(args[2])

        if '-z' in args:
            if os.path.isfile(args[2]):
                if 'True' in args:
                    t.tgz_uncompress(args[2], force=True)
                else:
                    t.tgz_uncompress(args[2])
    else:
        print (message)


if __name__ == '__main__':
    t = FileProcess()
    check_input(sys.argv)
