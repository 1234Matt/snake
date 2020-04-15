# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 04:19:09 2020

@author: 1234matt & mayor-slash
"""
import pygame
import numpy as np


WIN_WIDTH = 800 
WIN_HEIGHT = 600
box_size = 25
number_of_columns = int(WIN_WIDTH/box_size)
number_of_rows = int(WIN_HEIGHT/box_size)


screen = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT)) # initialize the game screen
pygame.display.set_caption("Snake Remake") # sets Game-Window Label
clock = pygame.time.Clock() # initalize the game clock

play = True



# creating gamefield matrix
game_field = np.zeros((number_of_columns, number_of_rows))


#def update_grid(screen,game_field):
    



while play:
    
    clock.tick(30) # Sets max frame-rate to 30
    
    
    for event in pygame.event.get(): # collects all user input events
            if event.type == pygame.QUIT: # exits game when mouse clicking exit
                play = False
                pygame.quit()
                break


