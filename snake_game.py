# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 04:19:09 2020

@author: Marius Neumann
"""
import pygame


WIN_WIDTH = 800 
WIN_HEIGHT = 600

screen = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT)) #initialize the game screen
pygame.display.set_caption("Snake Remake") #sets Game-Window Label
clock = pygame.time.Clock() #initalize the game clock

play= True

while play:
    
    clock.tick(30) #Sets max frame-rate to 30
    
    
    for event in pygame.event.get(): #collects all user input events
            if event.type == pygame.QUIT: # exits game when mouse clicking exit
                play = False
                pygame.quit()
                break



