#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os, sys
import commands

def find_file(path,formet):
    try:
        a = []
        fns = [os.path.join(root, fn) for root, dirs, files in os.walk(path) for fn in files]
        for f in fns:
            if os.path.isfile(f):
                if formet in f:
                    a.append(f)
        return a
    except IOError as o:
        print ('IOError',o)


def installPkg(pkg,disk):
    for i in pkg:
        result, output = commands.getstatusoutput("installer -pkg %s -target %s"%(i,disk))
        print ("Result: %s \n"%result)
        print ("Output: %s \n"%output)


if __name__ == '__main__':
    FilePath = os.path.dirname(sys.argv[0]) + "/Pkg"
    b = find_file(FilePath,".pkg")
    installPkg(b,"/Volum es/MaxDisk")