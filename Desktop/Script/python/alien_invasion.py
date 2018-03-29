#!/usr/bin/python

import sys
import pygame

class Settings():
    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)


def run_game():
    pygame.init()
    screen = pygame.display.set_mode((1200, 800))
    pygame.display.set_caption("Alien Invasion")

    bg_color = (230, 230, 230)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()


        screen.fill(bg_color)

        pygame.display.flip()
run_game()
