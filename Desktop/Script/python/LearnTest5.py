#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# -*- coding: GBK -*-

import difflib
import time
import os
import sys

Date = time.strftime("%Y_%m_%d_%H_%M_%S")

try:
    textfile1 = sys.argv[1]
    textfile2 = sys.argv[2]
except Exception,e:
    print "\033[0;31m" + "Error: " + str(e) + "\033[0m"
    print "\033[0;31m" + "Usage: " + str(sys.argv[0]) + " filename1 filename2" + "\033[0m"
    sys.exit(1)

def writefile(string,file):
    try:
        with open(file, 'a') as d:
            d.write(string + '\n')
    except IOError as i:
        print ('IOError:',i)

def readfile(filename):
    try:
        fileHandle = open (filename, 'rb')
        text = fileHandle.read().splitlines()
        fileHandle.close()
        return text
    except IOError as error:
        print ('Read file Error:' + str(error))
        sys.exit(1)

def running():
    text1_lines = readfile(textfile1)
    text2_lines = readfile(textfile2)

    txtpath = os.path.expanduser('~') + '/Desktop/' + Date + '.txt'
    htmlpath = os.path.expanduser('~') + '/Desktop/' + Date + '.html'

    f = difflib.Differ()
    diff = f.compare(text1_lines,text2_lines)
    f_result = str('\n'.join(list(diff)))
    writefile(f_result,txtpath)

    d = difflib.HtmlDiff()
    d_result = d.make_file(text1_lines,text2_lines)
    writefile(d_result,htmlpath)

    #print d_result

if __name__ == '__main__':
    if textfile1 == "" or textfile2 == "":
        print "\033[0;31m" + "Usage: " + str(sys.argv[0]) + " filename1 filename2" + "\033[0m"
        sys.exit(1)
    running()

