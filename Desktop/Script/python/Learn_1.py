#!/usr/bin/python

import csv
import Tkinter


def writefile(string,file):
    try:
        with open(file, 'a') as d:
            d.write(string + '\n')
    except IOError as i:
        print ('IOError_4:',i)

def createListCSV(fileName, dataList):
    with open(fileName, "a") as csvFile:
        w = csv.writer(csvFile)
        for data in dataList:
            w.writerow(data)
    csvFile.close


a = [ 1, 2, 3, 4, 5, 6, 7, 8, 9, 0 ]

#writefile(str(a[:]),"/Users/saseny/Desktop/12334.csv")


#csv.writer("/Users/saseny/Desktop/12334.csv" [,dialect=excel,[,**fmtparam]])

createListCSV("/Users/saseny/Desktop/12334.csv", a)
