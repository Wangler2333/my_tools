#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 10/28/17 4:41 PM
@author: Saseny Zhou
@File:   atm.py
"""

import os, sys

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(base_dir)

sys.path.append(base_dir)

from core import main

if __name__ == '__main__':
    main.run()
