#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import matplotlib
import pandas
import numpy



a = pandas.read_csv("/Users/saseny/Desktop/App_Test/Result/TestMainTime.csv")

a.to_excel("/Users/saseny/Desktop/App_Test/Result/123.xlsx")