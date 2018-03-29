#!/usr/bin/python

#import csv
import sys

File = "/Users/saseny/Desktop/5-11.40.0B2.txt"
File_="/Users/saseny/Desktop/Fislsjd.csv"
principal = 1000
rate = 0.05
numyears = 5
year = 1
#print  '\n' + File + '\n'

#f = open(File)
#line = f.readline()
#while line:
#    print line.lower(),
#    line = f.readline()
#f.close()

#for line in open(File):
#    print line

f = open(File_,"w")
while year <= numyears:
    principal = principal * (1 + rate)
    #print >>f, "%2d %0.2f" % (year,principal)
    f.write("%2d %0.2f\n" % (year,principal))
    year +=1
f.close()

#sys.stdout.write("Enter your name :")
#name = sys.stdin.readline()
#name = "My name is: " + name

#name = raw_input("Enter your name :")
#print name.title()

B = format(numyears,"0.5f")
#B = str(numyears)
#B = repr(numyears)
print B