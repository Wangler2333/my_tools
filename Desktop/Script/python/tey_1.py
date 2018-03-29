import sys
import matplotlib
import re

'''

reload(sys)
sys.setdefaultencoding('utf-8')


class Rectangle(object):
    def __init__(self,width,height):
        self.width = width
        self.height = height
    def area(self):
        return self.width * self.height
    #area = property(fget=_area)

    def _width(self):
        return self._width

    def _setWidth(self, width):
        self._width = width

    width = property(fget=_width, fset=_setWidth)

t = Rectangle(1,2)

print t.area
'''


import commands


TOTAL_DISK = USED_DISK = USED_DISK_PERCENT = FREE_DISK = FREE_DISK_PERCENT = None
a = commands.getoutput('diskutil info \"Macintosh HD\"')

total = re.findall(r'Volume Total Space:\s+(\d+\.\d?)', a)
used = re.findall(r'Volume Used Space:\s+(\d+\.\d?).*\((\d+\.\d?\%)\)', a)
available = re.findall(r'Volume Available Space:\s+(\d+\.\d?).*\((\d+\.\d?\%)\)', a)

if total:
    TOTAL_DISK = total[0]
if used:
    USED_DISK = used[0][0]
    USED_DISK_PERCENT = used[0][1]
if available:
    FREE_DISK = available[0][0]
    FREE_DISK_PERCENT = available[0][1]



print TOTAL_DISK,USED_DISK,USED_DISK_PERCENT,FREE_DISK,FREE_DISK_PERCENT