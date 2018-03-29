#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 10/28/17 4:52 PM
@author: Saseny Zhou
@File:   account_sample.py
"""

import json
import os

acc_dic = {
    'id': 1234,
    'password': 'abc',
    'credit': 15000,
    'balance': 15000,
    'enroll_date': '2017-10-1',
    'expire_date': '2021-01-01',
    'pay_day': 22,
    'status': 0  # 0 = normal , 1 = locked, 2 = disabled
}

print(json.dumps(acc_dic))

if not os.path.isfile('accounts/1234.json'):
    f = open('accounts/1234.json', 'w')
    f.write(json.dumps(acc_dic))
    f.close()
