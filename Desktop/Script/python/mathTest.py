#!/usr/bin/env python
# -*- coding: UTF-8 -*-


import math
import commands

b = commands.getoutput('ypc2 -rdk B0FC')
a = commands.getoutput('ypc2 -rdk B0RM')

c = (float(a) / float(b)) * 100
Battery_level = str(int(c)) + "%"


print Battery_level