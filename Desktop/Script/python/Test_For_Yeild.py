#!/usr/bin/env python
# coding=UTF-8
'''
使用生成器与协程。

'''

import os
import fnmatch

def find_files(topdir, pattern):
    for path, dirname, filelist in os.walk(topdir):
        for name in filelist:
            if fnmatch.fnmatch(name, pattern):
                yield os.path.join(path, name)


import gzip
import bz2

def opener(filenames):
    for name in filenames:
        if name.endswith(".gz"): f = gzip.open(name)
        elif name.endswith(".bz2"): f = bz2.BZ2File(name)
        else: f = open(name)
        yield f


def cat(filelist):
    for f in filelist:
        for line in f:
            yield line


def grep(pattern, lines):
    for line in lines:
        if pattern in line:
            yield line


b = find_files("/Users/saseny/Desktop/Log_For_Regression/Log/Runin\&Postburn","C02TM02JJ495")
b.next()