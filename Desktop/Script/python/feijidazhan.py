#coding=utf-8
import pygame
from pygame.locals import *
import random
import time
'''
思路：
定义基础飞机类:
	|--
继承基础飞机类，定义敌机、定义玩家；

子弹类、

步骤：
1、创建图形界面，加载背景图片，
2、

'''
#定义基础类，初始化坐标、图片
class Base(object):
	def __init__(self,x,y,planeImageName):
		self.x = x
		self.y = y
		self.image = pygame.image.load(planeImageName).convert()
	def draw(self):
		screen.blit(self.image,(self.x,self.y))

#定义基础飞机类，初始化：飞机名字、存储子弹、保存屏幕

class Plane(Base):
	def __init__(self,screen,planeName,planeImageName):
		Base.__init__(self,0,0,planeImageName)
		self.planeName = planeName
		self.screen = screen
		self.bulletList = []
	#将飞机显示出来，调用基础类的draw方法
	def draw(self):
		Base.draw(self)
		needRemoveList = []


if __name__ == '__main__':
	#定义图形界面,定义当前目录下的背景图片
	screen = pygame.display.set_mode((480,890),0,32)
	bgImageFile = './feiji/background.png'
	background = pygame.image.load(bgImageFile).convert()
	while True:
		screen.blit(background,(0,0))






