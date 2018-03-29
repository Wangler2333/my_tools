#!/usr/bin/python

Tip='''
The Zen of Python, by Tim Peters
Beautiful is better than ugly.
Explicit is better than implicit.
Simple is better than complex.
Complex is better than complicated.
Flat is better than nested.
Sparse is better than dense.
Readability counts.
Special cases aren't special enough to break the rules.
Although practicality beats purity.
Errors should never pass silently.
Unless explicitly silenced.
In the face of ambiguity, refuse the temptation to guess.
There should be one-- and preferably only one --obvious way to do it.
Although that way may not be obvious at first unless you're Dutch.
Now is better than never.
Although never is often better than *right* now.
If the implementation is hard to explain, it's a bad idea.
If the implementation is easy to explain, it may be a good idea.
Namespaces are one honking great idea -- let's do more of those!
'''

principal = 1000
rate = 0.05
numyears = 5
year = 1
a = 1
b = 2
print
while year <= numyears:
    principal = principal * (1 + rate)
    #print "%2d %0.3f" % (year, principal)
    #print format(year,"3d"),format(principal,"0.3f")
    print "{0:2d} {1:0.2f}".format(year,principal)
    year += 1
#a = year
if a < b:
    pass
else:
    print "Computer says No"

product = "game"
type = "pirate memory"
age = 5

print Tip.title()
print type.strip()

if product == "game" and type == "pirate memory" \
                     and not (age < 4 or age > 8):
                     print " I'll take it!"

suffix = ".htm"
if suffix == ".htm":
    content = "text/html"
elif suffix == ".jpg":
    content = "image/jpeg"
elif suffix == ".png":
    content = "image/png"
else:
    raise RuntimeError("Unknown content type")

spam = "122"
s = {1233,122,321}
if 'spam' in s:
    has_spam = True
else:
    has_spam = False



# has_spam = 'spam' in s


