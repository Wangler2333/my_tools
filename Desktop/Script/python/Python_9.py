#!/usr/bin/python

import sys
import time
import os
import csv
import tarfile

from subprocess import Popen, PIPE, check_output
from plistlib import readPlistFromString, readPlist
from pprint import pprint
from commands import *

FolderLine = []
TempPath = os.getcwd()
#print TempPath

def systemProfiler(types):
    systemProfilerXml=Popen(["system_profiler", types, "-xml"], stdout=PIPE).communicate()[0]
    pl=readPlistFromString(systemProfilerXml)
    return pl

def SP(types,item_to_check):
    return systemProfiler(types)[0]['_items'][0][item_to_check]

def Logcheck(LogPath,Patameter1):
    with open(LogPath) as f:
        for line in f:
            if Patameter1 in line:
                print line.split(',')[7] + ' , ' + line.split(',')[10] + ' , ' + line.split(',')[-4]

                #print line.split(',')[7]
                #print line.split(',')[10]
                #print line.split(',')[-4]


def Process(Path,format):
    for i in os.listdir(Path):
        Filepath = Path + '/' + i
        if not os.path.isfile(Filepath):
            for j in os.listdir(Filepath):
                if j.endswith(format):
                    if "FAIL" in j:
                        target = Filepath + '/' + j
                        t = tarfile.open(target,"r:gz")
                        for tinfo in t:
                            t.extract(tinfo.name, r'TempPath')
                        #t.close()
                        #os.popen('rm -rf $target')

def Filelist(path):
    fns = [os.path.join(root, fn) for root, dirs, files in os.walk(path) for fn in files]
    for f in fns:
        if os.path.isfile(f):
            if '.tgz' in f:
                print (f)
    print(len(fns))



    a = []
    a.a




#print SP("SPHardwareDataType","boot_rom_version")

#print Process("/Users/saseny/Desktop/Log_For_Regression/OUT/122",".tgz")
#print Logcheck("/Users/saseny/Desktop/processlog.plog","FAIL-UPDA")
print Filelist("/Users/saseny/Desktop/LOG")