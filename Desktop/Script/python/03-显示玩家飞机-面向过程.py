#coding=utf-8
import pygame
from pygame.locals import *


if __name__ == "__main__":

    #1. 创建一个窗口，用来显示内容
    screen = pygame.display.set_mode((480,890),0,32)

    #2. 创建一个和窗口大小的图片，用来充当背景
    background = pygame.image.load("./feiji/background.png").convert()

    #测试，用来创建一个玩家飞机的图片
    hero = pygame.image.load("./feiji/hero.gif").convert()



    x=0
    y=0

    #3. 把背景图片放到窗口中显示
    while True:
        screen.blit(background,(0,0))
        screen.blit(hero,(x,y))



        #判断是否是点击了退出按钮
        for event in pygame.event.get():
            # print(event.type)
            if event.type == QUIT:
                print("exit")
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_a or event.key == K_LEFT:
                    print('left')
                    #控制飞机让其向左移动
                    x-=5
                elif event.key == K_d or event.key == K_RIGHT:
                    print('right')
                    x+=5
                elif event.key == K_SPACE:
                    print('space')
        pygame.display.update()
