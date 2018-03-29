#!/usr/bin/python

import sys

if len(sys.argv) != 2:
  print "Please supply a filename:"
  raise SystemExit(1)
f = open(sys.argv[1])
lines = f.readlines()
f.close()

fvalues = [float(lines) for line in lines]

print "The minimum value is ", min(fvalues)
print "The maximum value is ", max(fvalues)
