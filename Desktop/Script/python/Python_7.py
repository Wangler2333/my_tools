#!/usr/bin/python

for n in [1,2,3,4,5,6,7,8,9]:
    print "2 to the %d power is %d" % (n, 2**n)


for n in range(1,10):
    print "2 to the %d power is %d" % (n, 2 ** n)


def Count(n):
    print "Counting down!"
    while n > 0:
        yield n
        n -= 1
for i in Count(5):
    print i

