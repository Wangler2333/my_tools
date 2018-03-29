#!/usr/bin/env python
# coding: UTF-8

import wx
import os, sys
import Queue
import threading
import time, random
import commands
import re


q = Queue.Queue(0)
NUM_WORKERS = 1
mylock = threading.Lock()

passwd_file = os.path.expanduser('~') + '/passwd.txt'
decode_cmd = os.path.dirname(sys.argv[0]) + '/Decode.sh'
tmp_file = '/tmp/passwd.txt'



os.system('%s' % decode_cmd)

        with open(pass_file) as fd:
            for line in fd:
                if "PDCAIP:" in line:
                    PDCAIPAdress = str(line).split('PDCAIP:')[1].replace('\n', '')
                if "PDCAAccount:" in line:
                    UserName = str(line).split('PDCAAccount:')[1].replace('\n', '')
                if "PDCAPassword:" in line:
                    PassWord = str(line).split('PDCAPassword:')[1].replace('\n', '')

