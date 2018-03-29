#!/usr/bin/env python

import sys
import time

for i in range(100):
   sys.stdout.write(".")
   time.sleep(1)
   sys.stdout.flush()
