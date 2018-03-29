#!/usr/bin/python

import time

File = "/Users/saseny/Desktop/5-11.40.0B2.txt"

def tail(f):
    f.seek(0,2)
    while True:
        line = f.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line

def grep(lines, searchtext):
    for line in lines:
        if searchtext in line: yield line

wwwlog = tail(open(File))
pylines = grep(wwwlog, "Z0TV005Z")
for line in pylines:
    print line,