#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import sys
import commands
import time
from subprocess import Popen, PIPE
from plistlib import readPlistFromString
import matplotlib.pyplot as plt


y_values = [' 40.000000', ' 48.000000', ' 48.125000', ' 48.250000', ' 48.125000', ' 48.250000', ' 60.250000', ' 48.375000', ' 48.250000', ' 48.000000']
a = len(y_values)
x_values = list(range(a))
plt.ylim((0,100))

plt.plot(x_values, y_values, linewidth=2)

plt.title("Temperature Numbers", fontsize=24)
plt.xlabel("Times", fontsize=14)
plt.ylabel("Temperature", fontsize=14)

plt.tick_params(axis='both', labelsize=14)
plt.savefig('Temperature.png', bbox_inches='tight')
plt.show()
