#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time     : 2017/11/14上午11:11
# @Author   : Saseny Zhou
# @Site     : 
# @File     : error_code.py
# @Software : PyCharm Community Edition

import numpy as np
import pandas as pd
import xlrd
import xlwt

# from pyExcelerator import *
# from Workbook import *


file = '/Users/saseny/Desktop/ERROR.xlsx'
df = pd.read_excel(file, encoding='gbk')

dk = xlrd.open_workbook(file, encoding_override='gbk')
shxrange = range(dk.nsheets)

try:
    sh = dk.sheet_by_name('Error Codes')

except:
    print('No sheet in %s named Sheet1' % file)

nrows = sh.nrows
ncols = sh.ncols

print('nrows %d, ncols %d' % (nrows, ncols))

cell_value = sh.cell_value(42, 4)

print(cell_value)

row_list = []

for i in range(1, nrows):
    row_data = sh.row_values(i)
    print(row_data[2:5])
    row_list.append(row_data)

# print(row_list)
