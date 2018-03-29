#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# __author__: Saseny Zhou


class Rectangle(object):
    def __init__(self, width=None, height=None):
        self.width = width
        self.height = height

    def _area(self):
        b = self.width * self.height
        return b

    area = property(fget=_area)


t = Rectangle(width=5,height=4)
print t.width, t.height, t.area
t.width = 6
print t.width, t.height, t.area