# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 04:19:09 2020

@author: Marius Neumann
"""
import pygame


WIN_WIDTH = 800
WIN_HEIGHT = 600

screen = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
pygame.display.set_caption("Snake Remake")
clock = pygame.time.Clock()

play= True

while play:
    
    clock.tick(30)
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = False
                pygame.quit()
                break



