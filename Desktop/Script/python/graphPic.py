# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import matplotlib
import matplotlib.dates as mdate
import matplotlib.ticker as mtick
import numpy as np
import pandas as pd
import os

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False


class graph(object):
    def __init__(self, savePath=None):
        self.path = savePath

    def contentCheck(self, info, number):
        if info == 'Yield':
            self.title = '良率报告'
            self.xLabel = '站别'
            self.yLabel = '良率 %'
            self.target = []
            for i in range(1, int(number) + 1, 1):
                self.target.append(95)
            self.x_axle = []

        elif info == 'RetestRate':
            self.title = 'Retry报告'
            self.xLabel = '站别'
            self.yLabel = 'RetryRate %'
            self.target = []
            for i in range(1, int(number) + 1, 1):
                self.target.append(3)

        self.x_axle = []
        for j in range(1, int(number) + 1, 1):
            self.x_axle.append(j)

    def open(self, *args):
        self.contentCheck(args[0], args[1])  # plt.rc('xtick', labelsize=15)  plt.rc('ytick', labelsize=15)

        plt.plot(self.x_axle, args[2], linewidth=2, label=args[0], rotation=45)
        # plt.plot(self.x_axle, self.target, linewidth=2, label='Target')
        plt.xticks(self.x_axle, args[3], rotation=0)

        plt.title(self.title, fontsize=24)
        plt.xlabel(self.xLabel, fontsize=14)
        plt.ylabel(self.yLabel, fontsize=14)

        plt.legend(loc='upper left')

        fig = matplotlib.pyplot.gcf()
        fig.set_size_inches(11.8, 8.2)
        fig.savefig(self.path + '/squares_plot.png', bbox_inches='tight', dpi=100)


if __name__ == '__main__':
    pass
