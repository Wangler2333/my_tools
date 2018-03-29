#!/usr/bin/python

names = []
names = list()

names = [ "Dave", "Dark", "Ann", "Phil" ]
a = names[2]

print a + '\n'

names[0] = "Jeff"

print names

names.append("Paula")
# Add to the last

print names

names.insert(2, "Thomas")
# Add parameter

print names

b = names[0:2]
print b

c = names[2:]
print c

names[0:2] = [ "Dave", "Mark", "Jeff" ]
print names
