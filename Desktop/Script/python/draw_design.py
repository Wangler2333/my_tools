#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 10 11:25:34 2017

@author: saseny
"""

import turtle


class draw_design(object):
    def __init__(self):
        self.window = turtle.Screen()
        self.babbage = turtle.Turtle()
        self.draw_stem_centre()
        
    def draw_stem_centre(self):
        self.babbage.left(90)
        self.babbage.forward(100)
        self.babbage.right(90)
        self.babbage.circle(10)
        
    def draw_petal(self,cycle=23):
        for i in range(cycle):
            self.draw_color()
            self.babbage.left(15)
            self.babbage.forward(50)
            self.babbage.left(157)
            self.babbage.forward(50)  
        self.close_window()   
        
    def draw_color(self):
        if self.babbage.color() == ("red", "black"):
            self.babbage.color("orange", "black")
        elif self.babbage.color() == ("orange", "black"):
            self.babbage.color("yellow", "black")
        else:
            self.babbage.color("red", "black")
            
    def close_window(self):
        self.babbage.hideturtle()
        self.window.exitonclick()        

 
if __name__ == '__main__':    
    t = draw_design()
    t.draw_petal(cycle=92)    