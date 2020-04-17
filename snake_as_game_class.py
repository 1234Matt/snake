# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 04:19:09 2020

@author: 1234matt & mayor-slash
"""
import pygame
import numpy as np
import random


WIN_WIDTH = 800 
WIN_HEIGHT = 600
box_size = 15
play_field_width = WIN_WIDTH-40
play_field_height= WIN_HEIGHT-100
number_of_columns = int(play_field_width/box_size)
number_of_rows = int(play_field_height/box_size)
game_field_x0 = 20
game_field_y0 = 80
game_field_x1 = game_field_x0 + box_size*(number_of_columns-1)
game_field_y1 = game_field_y0 + box_size*(number_of_rows-1)




screen = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT)) # initialize the game screen
pygame.display.set_caption("Snake Remake") # sets Game-Window Label
clock = pygame.time.Clock() # initalize the game clock
pygame.init()

play = True





# dictonary to store the values which will be in the game_field matrix according to their color-string
color_index = {"white" : 1,
          "black": 0,
          "red": 2,
          "green":3
          
          }

# dictonary to store the rgb tuples according to the values in the game_field matrix
index_tuple = {1:(255, 255, 255),
               0:(0, 0, 0),
               2:(255, 0, 0),
               3:(0, 255, 0)
               }


#make textboxes
font = pygame.font.Font(None,80)
font_color = index_tuple[1]
font_background = index_tuple[0]
#Gen = font.render("Generation: "+ str(gen),True,font_color)
#Alive = font.render("Alive: "+str(50),True,font_color)
Score = font.render("Score: ",True,font_color)

#Gen_rect = Gen.get_rect()
#Alive_rect = Alive.get_rect()
Score_rect = Score.get_rect()

#Gen_rect.top = 50
#Gen_rect.left = 50
#Alive_rect.top = 120
#Alive_rect.left = 50
Score_rect.top = 5
Score_rect.left = 5

# 4 different directions the snake can move, by pressing left/right arrow key you can cycle through this directions
directions = [
    np.array((1,0)),
    np.array((0,-1)),
    np.array((-1,0)),
    np.array((0,1))
    ]


#creating a class of a Game, that way we can recall a Game after one finishes (and maybe use the Neat-module to train some AIs)
class Game:
    
    #each game comes with its own game_field and own snake
    def __init__(self):
        self.game_field = np.zeros((number_of_rows, number_of_columns))
        self.snake = Snake()
        self.item = Item(self.snake.snake_position,self.snake.snake_body)
        self.score = 0
        
    #displays the current game_field onto the screen
    def update_grid(self,screen):
        y = game_field_y0
        for row in self.game_field:
            x = game_field_x0
            for box in row:
                rect = pygame.Rect(x, y, box_size, box_size)
                color = index_tuple[box]
                pygame.draw.rect(screen,color,rect)
                x += box_size
            y += box_size
        
        
        
    #main method which will be called inside the main-loop
    def play(self,screen,display_game=False):
        # clears the entire game_field to zeros (makes everything black)
        self.game_field = np.zeros((number_of_rows, number_of_columns))
        
        # moves the snake head
        self.game_field,item_found = self.snake.move(time,self.game_field,self.item.position)
        
        #create new item if last was found
        if item_found:
            self.item = Item(self.snake.snake_position,self.snake.snake_body)
            self.score += 1
        
        #draw item onto game_field
        self.draw_item()
        
        # displays the snake body (the places where the snake has been earliere)
        self.game_field = self.snake.pass_body(self.game_field)
        
        if display_game:
            
            # draws grid 
            self.update_grid(screen)
            
            #draws frame of play_field
            self.draw_game_field(screen)
            
            # update screen
            pygame.display.update()
        
    def draw_item(self):
        self.game_field[self.item.position[0]][self.item.position[1]]=self.item.color
        
    def draw_game_field(self,screen):
        pygame.draw.line(screen,index_tuple[1],(game_field_x0,game_field_y0),(game_field_x1,game_field_y0),2)
        pygame.draw.line(screen,index_tuple[1],(game_field_x1,game_field_y0),(game_field_x1,game_field_y1),2)
        pygame.draw.line(screen,index_tuple[1],(game_field_x1,game_field_y1),(game_field_x0,game_field_y1),2)
        pygame.draw.line(screen,index_tuple[1],(game_field_x0,game_field_y1),(game_field_x0,game_field_y0),2)
        
        #Gen = font.render("Generation: "+ str(gen),True,font_color)
        #Alive = font.render("Alive: "+str(len(players)),True,font_color)
        Score = font.render("Score: "+str(self.score),True,font_color)
        
        #screen.blit(Gen,Gen_rect)
        #screen.blit(Alive,Alive_rect)
        screen.blit(Score,Score_rect)
#creating class Item 
class Item:
    
    def __init__(self,snake_position,snake_body):
        found = False
        while not found:
            x = random.randint(0,number_of_rows-2)
            y = random.randint(0,number_of_columns-2)
            d = np.sqrt((x-snake_position[0])**2 + (y - snake_position[1])**2)
            
            if d>5:
                overlapp = False
                for bodypart in snake_body:
                    if x == bodypart[0] and y==bodypart[1]:
                        overlapp = True
                if not overlapp:
                    found = True
        
        self.position = np.array((x,y))
        self.color = color_index["green"]
        
           


#creating class Snake. The Snake obkject will be an attribut of the Game object
class Snake:


    def __init__(self,color_head="red",color_body ="white"):
        self.snake_color = color_index[color_head]  # color of the snake_head is standart red, but could be changed by calling Snake object with extra string arguments
        self.snake_length = 5  # starting length of snake, will later be increased by "eating" fruits
        self.snake_direction = 0 # starting index in the directions_list
        self.snake_position = np.array((5, 7)) # starting position of the snake head as array so we can use vector additions later
        self.snake_body_color = color_index[color_body] # color of the snake_body is standart white, but could be changed by calling Snake object with extra string arguments
        self.snake_body = [] # empty list where the previous positions of the head and therefor the body is stored
        self.dead = False
        self.frames_per_movement = 10
        
    def move(self,time,game_field,item_position):
        # only moves snake head every 20 timesteps. Could definitly use a better solution here!
        item_found = False
        if time%self.frames_per_movement ==0:  
            #creates copy of snake_positions 
            old = self.snake_position.copy()
            
            
            
            #changes snake_position depending to the current direction(vector addition)
            self.snake_position += directions[self.snake_direction]
            
            #check for collisions
            item_found = self.collision(item_position)
            
            self.snake_body.append(old)
            
        #draws snake head reagardless of if it moved or not
        game_field[self.snake_position[0]][self.snake_position[1]]=self.snake_color
            
        return game_field,item_found


    
    def pass_body(self,game_field):
        
        #deletes the first object ("snake tail") if the list of snake parts is longer then the snake length
        if len(self.snake_body)>self.snake_length:
            self.snake_body.remove(self.snake_body[0])
        
        #iterates through all bodyparts of the snake and draws them to the gamefield
        for bodypart in self.snake_body:
            game_field[bodypart[0]][bodypart[1]]=self.snake_body_color
            #print(bodypart[0])
            #print(bodypart[1])
        return game_field
    
    def collision(self,item_position):
        x = self.snake_position[0]
        y = self.snake_position[1]
        item_found = False
        #check for collision with itself
        for bodypart in self.snake_body:
            bodypart_x = bodypart[0]
            bodypart_y = bodypart[1]
            
            if x==bodypart_x and y == bodypart_y:
                print("collision with self")
                self.dead = True
                return item_found
        
        #check for collision with wall
        
        
        if x<0 or x>number_of_rows-2 or y<0 or y>number_of_columns-2:
            self.dead = True
            print("collision with wall")
            return item_found
         
        
        #check for collection of item
        if np.array_equal(self.snake_position,item_position):
            self.snake_length +=1
            item_found = True
            self.frames_per_movement -=1
            if self.frames_per_movement <1:
                self.frames_per_movement=1
            
        return item_found
            
        
    

    
    

        

#set time to zero and create new Game object with new snake
time = 0
game1 = Game()
while play and not game1.snake.dead:
    
    clock.tick(30) # Sets max frame-rate to 30
    time += 1 # increases timestep by 33.33 ms due to the frame_rate
    screen.fill(index_tuple[0])
    
    
    
    for event in pygame.event.get(): # collects all user input events and iterates through them
            if event.type == pygame.QUIT: # exits game when mouse clicking exit
                play = False
                pygame.quit()
                quit()
                break
            # if the event is a pressed Key, check if its the left or right arrow key
            elif event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_LEFT:
                    # changes direction by subtracting 1 from it. using "%4" to make 4 = 0 
                    game1.snake.snake_direction = (game1.snake.snake_direction -1)%4
                elif event.key == pygame.K_RIGHT:
                    # changes direction by adding 1 to it. using "%4" to make 4 = 0 
                    game1.snake.snake_direction = (game1.snake.snake_direction +1)%4
    
    game1.play(screen,True)

try:
    pygame.quit()
    
except:
    print("game over")
