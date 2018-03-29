#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import pygame
import sys
import _thread


pygame.init()
size = width, height = 1000, 800
speed = [-200, 100]
bg = (255, 255, 255)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("初次见面，请大家多多关照!")
turtle = pygame.image.load('/Users/saseny/Desktop/123.png')
position = turtle.get_rect()


def move_pic(position,turtle):
    while True:
        #for event in range(1000): #pygame.event.get():
            #if event.type == pygame.QUIT:
            #    sys.exit()
            position = position.move(speed)
            if position.left < 0 or position.right > width:
                turtle = pygame.transform.flip(turtle, True, False)
                speed[0] = - speed[0]
            if position.top < 0 or position.bottom > height:
                speed[1] = - speed[1]

            screen.fill(bg)
            screen.blit(turtle, position)
            pygame.display.flip()
            pygame.time.delay(0)


move_pic(position,turtle)