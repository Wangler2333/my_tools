#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 10/28/17 4:45 PM
@author: Saseny Zhou
@File:   logger.py
"""

import logging
from conf import settings

def logger(log_type):
    logger = logging.getLogger(log_type)
    logger.setLevel(settings.LOG_LEVEL)

    ch = logging.StreamHandler()
    ch.setLevel(settings.LOG_LEVEL)