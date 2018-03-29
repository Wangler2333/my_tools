#!/usr/bin/python

import json

Path = "/Users/sasenyzhou/Desktop/123/C02T8FR6GTFJ_IP.log"


a = []
b = []

def Check_Log(Path):
    with open(Path) as msg:
        date = json.load(msg)
        print date

def Chec_Log(Path,Patameter2):
    with open(Path) as msga:
        for line_ in msga:
            if "=" in line_:
                if Patameter2 in line_:
                    print line_
                #    b.append(line_.split('"')[1])

def load(filr):
    with open(filr) as json_file:
        data = json.load(json_file)
        return data


Check_Log(Path)
print "---------------------"
#Chec_Log(Path,"value")


print a
print len(a)
print "---------------------"
print b

#load("/Users/sasenyzhou/Desktop/123/C02T8FR6GTFJ.json")

