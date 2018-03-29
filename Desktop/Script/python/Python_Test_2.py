#!/usr/bin/python

import sys

Says = []
fvalues = []

if len(sys.argv) != 2:
    print "Please supply a filename."
    raise SystemExit(1)

for line in open(sys.argv[1]):
    fields = line.split()
    for i in fields:
        Says.append(i)

print Says

for i in Says:
    fvalues.append(float(i))

fvalues.sort(reverse=True)
print fvalues
print "There have " + str(len(fvalues)) + " parameter in set 'fvalues'."


print "The minimum value is ", min(fvalues)
print "The maximum value is ", max(fvalues)