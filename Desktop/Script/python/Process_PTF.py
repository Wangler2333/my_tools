#!/usr/bin/python
# Create on 2017/03/16

import json
import sys
import os

def writefile(string,file):
    try:
        with open(file, 'a') as d:
            d.write(string + '\n')
    except IOError as i:
        print ('IOError_4:',i)

def Check_OutFile(file):
    try:
        if not os.path.isfile(file):
            title = "Test Item, Error Code, Test Info, Message"
            writefile(title,file)
    except TypeError as h:
        print ('TypeError_1:',h)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        filename = raw_input("Pls input file path road:")
    else:
        filename = sys.argv[1]
    filepath = os.path.dirname(sys.argv[0]) + "/_result.csv"
    with open(filename) as obj:
        numbers = json.load(obj)
    dd = len(numbers[u'data'][u'tests'])
    ac = []
    dicts = {}
    dicts = numbers[u'data']
    no = 0
    Check_OutFile(filepath)
    while no < dd:
        try:
            a = numbers[u'data'][u'tests'][no][u'category']
            b = numbers[u'data'][u'tests'][no][u'key']
            d = numbers[u'data'][u'tests'][no][u'name']
            e = numbers[u'data'][u'tests'][no][u'description']
            c = str(a) + "," + str(b) + "," + str(d.replace(',', '')) + "," + str(e.replace(',', ''))
            writefile(c,filepath)
            no += 1
        except IndexError as e:
            print ('IndexError:',e)
