#coding=utf-8
import pygame



if __name__ == "__main__":

    #1. 创建一个窗口，用来显示内容
    screen = pygame.display.set_mode((480,890),0,32)

    #2. 创建一个和窗口大小的图片，用来充当背景
    background = pygame.image.load("./feiji/background.png").convert()

    #3. 把背景图片放到窗口中显示
    while True:
        screen.blit(background,(0,0))
        pygame.display.update()
