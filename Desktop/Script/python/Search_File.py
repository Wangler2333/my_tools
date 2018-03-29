#!/usr/bin/python

import os
import sys

def Display():
    print "-------------------------------"
    print "            DONE               "
    print "-------------------------------"

def Write_S(String):
    with open(path_road, 'a') as f:
        f.write(String + '\n')

def Search(path, fromt):
    fns = [os.path.join(root, fn) for root, dirs, files in os.walk(path) for fn in files]
    for f in fns:
        if os.path.isfile(f):
            if fromt in f:
                print f
                Write_S(f)

path_road = os.path.dirname(sys.argv[0]) + '/' + "SearchResult.txt"
if len(sys.argv) != 3:
    print "Input wrong parameter, need two parameter, one:(path road) and two:(search suffix name)!"
    Path = raw_input("Pls input search Path road: ")
    Fromt_ = raw_input("Pls input search suffix name: ")
    Fromt_ = "." + Fromt_
    print "-------------------------------"
    Search(Path,Fromt_)
    Display()
else:
    Path = sys.argv[1]
    Fromt_ = "." + sys.argv[2]
    print "-------------------------------"
    Search(Path,Fromt_)
    Display()

#if len(sys.argv) == 4:
