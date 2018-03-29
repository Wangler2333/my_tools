#!/usr/bin/python

import csv


def read_csv(file1,paratemer):
    csv_read = file(file1, 'r')
    for line in csv_read:
        if paratemer in line:
            print line.rstrip()


def open_file(file,patameter):
    with open(file) as messag:
        for line in messag:
            if patameter in line:
                print line.split()[4]







read_csv("/Users/saseny/Desktop/python_test.csv","C02T2001HT7F")

#open_file("/Users/saseny/Desktop/Unitsinfo.txt")



