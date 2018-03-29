#coding=utf-8
import pygame
from pygame.locals import *


#接下来要做的任务：
#1. 实现飞机在你想要的位置显示
#2. 实现按键控制飞机移动
#3. 实现按下空格键的时候，显示一颗子弹


class HeroPlane(object):

    def __init__(self,screen):

        #设置飞机默认的位置
        self.x = 230
        self.y = 600
        
        #设置要显示内容的窗口
        self.screen = screen


        self.imageName = "./feiji/hero.gif"

        self.image = pygame.image.load(self.imageName).convert()


        self.bullet = []


    def display(self):
        self.screen.blit(self.image,(self.x,self.y))



    def moveLeft(self):
        self.x -= 10


    def moveRight(self):
        pass


    def sheBullet(self):
        pass


if __name__ == "__main__":

    #1. 创建一个窗口，用来显示内容
    screen = pygame.display.set_mode((480,890),0,32)

    #2. 创建一个和窗口大小的图片，用来充当背景
    background = pygame.image.load("./feiji/background.png").convert()


    #3. 创建一个飞机对象
    heroPlane = HeroPlane(screen)


    #3. 把背景图片放到窗口中显示
    while True:
        screen.blit(background,(0,0))

        heroPlane.display()

        #判断是否是点击了退出按钮
        for event in pygame.event.get():
            # print(event.type)
            if event.type == QUIT:
                print("exit")
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_a or event.key == K_LEFT:
                    print('left')
                    heroPlane.moveLeft()
                    #控制飞机让其向左移动
                elif event.key == K_d or event.key == K_RIGHT:
                    print('right')
                elif event.key == K_SPACE:
                    print('space')

        pygame.display.update()
