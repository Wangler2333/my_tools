#!/usr/bin/python

import json
import sys
import os


if len(sys.argv) == 1:
    filename = raw_input("Pls input file path road:")
else:
    filename = sys.argv[1]

filepath = os.path.dirname(sys.argv[0]) + "/_result.csv"

def writefile(string,file):
    try:
        with open(file, 'a') as d:
            d.write(string + '\n')
    except IOError as i:
        print ('IOError_4:',i)


with open(filename) as obj:
    numbers = json.load(obj)
dd = len(numbers[u'data'][u'tests'])

ac = []
dicts = {}

#print type(numbers[u'data'][u'tests'])

dicts = numbers[u'data']
#print dicts.keys()

no = 0

while no < dd:
    try:
        a = numbers[u'data'][u'tests'][no][u'category']
        b = numbers[u'data'][u'tests'][no][u'key']
        d = numbers[u'data'][u'tests'][no][u'name']
        e = numbers[u'data'][u'tests'][no][u'description']
        c = str(a) + "," + str(b) + "," + str(d.replace(',', '')) + "," + str(e.replace(',', ''))
        #print c
        writefile(c,filepath)
        no += 1
    except IndexError as e:
        print ('IndexError:',e)
