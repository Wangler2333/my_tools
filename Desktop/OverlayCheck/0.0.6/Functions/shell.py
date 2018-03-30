#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time     : 2017/12/9上午10:15
# @Author   : Saseny Zhou
# @Site     : 
# @File     : shell.py
# @Software : PyCharm Community Edition


import subprocess
from Functions.copy_file import *


def shell(cmd):
    try:
        run = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        while run.poll() is None:
            print(run.stdout.readline())
        return_code = run.returncode
        return_list = [str(x).replace('\n', '') for x in run.stdout.readlines()]
        return return_code, return_list
    except IOError as e:
        print('IOError', e)


def download_running(args, tmp, product):
    cmd = os.path.join(os.path.dirname(tmp), args['download']['cmd link'])
    code, _ = shell(cmd)
    if code == 0:
        result = copy_file(os.path.join(os.path.expanduser('~'), 'Downloads'), args['download']['file key'], tmp,
                           args['download']['suffix'])
        if result is True:
            return True
        else:
            return False
    else:
        return False


class FileProcess(object):
    '''
    Usage:
          for file compress and uncompress
          now only can use for tgz formt
    '''

    def __init__(self):
        self.compress = 'cd %s; tar -zcvf %s %s &>/dev/null'
        self.uncompress = 'cd %s; tar -xzf %s &>/dev/null'

    def tgz_compress(self, obj, force=False):
        '''
        :param obj:     file path for compress
        :param force:   force to remove obj file when force is True
        :return:        no return
        '''
        path = os.path.dirname(obj)
        name = os.path.basename(obj)
        final = ".".join([name, "tgz"])
        a, b = shell(self.compress % (path, final, name))
        if force and a == 0:
            os.system('rm -rf %s' % obj)

    def tgz_uncompress(self, obj, force=False):
        '''
        :param obj:     file path for uncompress
        :param force:   force to remove obj file when force is True
        :return:        no return
        '''
        path = os.path.dirname(obj)
        name = os.path.basename(obj)
        a, b = shell(self.uncompress % (path, name))
        if force and a == 0:
            os.system('rm -rf %s' % obj)
