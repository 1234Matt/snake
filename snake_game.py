# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 04:19:09 2020

@author: 1234matt & mayor-slash
"""
import pygame
import numpy as np


WIN_WIDTH = 800 
WIN_HEIGHT = 600
box_size = 15
number_of_columns = int(WIN_WIDTH/box_size)
number_of_rows = int(WIN_HEIGHT/box_size)

#colors
white = (255, 255, 255)
black = (0, 0, 0)


screen = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT)) # initialize the game screen
pygame.display.set_caption("Snake Remake") # sets Game-Window Label
clock = pygame.time.Clock() # initalize the game clock

play = True



# creating gamefield matrix
game_field = np.zeros((number_of_rows, number_of_columns))
game_field[5][7]=1



#interates game_field matrix and updates screen according to values
def update_grid(screen,game_field):
    x = 0
    y = 0
    for row in game_field:
        x = 0
        for box in row:
            rect = pygame.Rect(x, y, box_size, box_size)
            if box == 1:
                pygame.draw.rect(screen, white, rect)
            else:
                pygame.draw.rect(screen, black, rect)
            x += box_size
        y += box_size
    pygame.display.update()
        



while play:
    
    clock.tick(30) # Sets max frame-rate to 30
    update_grid(screen,game_field)
    
    for event in pygame.event.get(): # collects all user input events
            if event.type == pygame.QUIT: # exits game when mouse clicking exit
                play = False
                pygame.quit()
                break


