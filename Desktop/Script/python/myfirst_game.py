#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
import easygui as g
import sys


def factorial(n):
    '''
       递归函数, 求阶乘.
    '''
    if n == 1:
        return 1
    else:
        return n * factorial(n - 1)


def fab(n):
    if n < 1:
        print('输入有误!')
        return -1
    if n == 1 or n == 2:
        return 1
    else:
        return fab(n - 1) + fab(n - 2)


# print (os.name)
# for i in os.walk('/Users/saseny/Desktop/2'):
#    print (i)


class gui(object):
    def __init__(self):
        g.msgbox('嗨，欢迎进入第一个界面小游戏^_^', image='/Users/saseny/Desktop/123.png')
        self.onbattun()

    def onbattun(self):
        msg = "请问你希望在鱼C工作室学习到什么知识呢？"
        title = "小游戏互动"
        choices = ["谈恋爱", "编程", "OOXX", "琴棋书画"]
        choices = g.choicebox(msg, title, choices)

        g.msgbox("你的选择是：" + str(choices), "结果")

        self.msg = "你希望重新开始小游戏吗？"
        self.title = "请选择"
        self.choose()

    def choose(self):
        if g.ccbox(self.msg, self.title, image='/Users/saseny/Desktop/123.png'):
            self.onbattun()
        else:
            sys.exit(0)


t = gui()
