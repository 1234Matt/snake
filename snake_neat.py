import numpy as np
import neat
import os
import random
import pygame




WIN_WIDTH = 1600
WIN_HEIGHT = 1000
box_size = 40
play_field_width = WIN_WIDTH-40
play_field_height= WIN_HEIGHT-100
number_of_columns = int(play_field_width/box_size)
number_of_rows = int(play_field_height/box_size)-1
game_field_x0 = 20
game_field_y0 = 80
game_field_x1 = game_field_x0 + box_size*(number_of_columns-1)
game_field_y1 = game_field_y0 + box_size*(number_of_rows-1)




screen = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT)) # initialize the game screen
pygame.display.set_caption("Snake Remake") # sets Game-Window Label
clock = pygame.time.Clock() # initalize the game clock
pygame.init()

play = True
time = 0




# dictonary to store the values which will be in the game_field matrix according to their color-string
color_index = {"white" : 1,
          "black": -1,
          "red": 2,
          "green":-2
          
          }

# dictonary to store the rgb tuples according to the values in the game_field matrix
index_tuple = {1:(255, 255, 255),
               -1:(0, 0, 0),
               2:(255, 0, 0),
               -2:(0, 255, 0)
               }


#make textboxes
font = pygame.font.Font(None,60)
font_color = index_tuple[1]
font_background = index_tuple[-1]
Gen = font.render("Generation: "+str(0),True,font_color)
Alive = font.render("Alive: "+str(50),True,font_color)
Score = font.render("Score: ",True,font_color)
Killer = font.render("Dead in: ",True,font_color)

Gen_rect = Gen.get_rect()
Alive_rect = Alive.get_rect()
Score_rect = Score.get_rect()
Killer_rect = Killer.get_rect()

Gen_rect.top = 5
Gen_rect.left = 200
Alive_rect.top = 5
Alive_rect.left = 600
Score_rect.top = 5
Score_rect.left = 5
Killer_rect.top = 5
Killer_rect.left = 900

# 4 different directions the snake can move, by pressing left/right arrow key you can cycle through this directions
directions = [
    np.array((1,0)),
    np.array((0,-1)),
    np.array((-1,0)),
    np.array((0,1))
    ]


kill_timer = 1000

#creating a class of a Game, that way we can recall a Game after one finishes (and maybe use the Neat-module to train some AIs)
class Game:
    
    #each game comes with its own game_field and own snake
    def __init__(self):
        self.game_field = -1 * np.ones((number_of_rows, number_of_columns))
        self.snake = Snake()
        self.items = [Item(self.snake.snake_position,self.snake.snake_body)]
        self.score = 0
        self.timer = 0
        
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
        
    def update_items(self):
        if len(self.items)<5:
            self.items.append(Item(self.snake.snake_position,self.snake.snake_body))
        
    #main method which will be called inside the main-loop
    def play(self,screen,display_game=False):
        self.timer += 1
        
        self.update_items()
        # clears the entire game_field to zeros (makes everything black)
        self.game_field = -1 * np.ones((number_of_rows, number_of_columns))
        
        # moves the snake head
        self.game_field,item_found,coll,index = self.snake.move(time,self.game_field,self.items)
        
        #create new item if last was found
        if item_found:
            self.items.pop(index)
            self.score += 1
            self.timer = 0
        
        if self.timer > kill_timer:
            coll = True
            print("Took to long --> Dead")
        #draw item onto game_field
        self.draw_item()
        
        # displays the snake body (the places where the snake has been earliere)
        self.game_field = self.snake.pass_body(self.game_field)
        
        inputData = self.gather_input()
        if display_game:
            
            # draws grid 
            self.update_grid(screen)
            
            #draws frame of play_field
            self.draw_game_field(screen)
            
            # update screen
            pygame.display.update()
            
        return item_found,coll,inputData
    
    
    def gather_input(self,size=3):
        inputDataPositions = []
        inputDataValues = []
        center = self.snake.snake_position
        front = directions[self.snake.snake_direction]
        left = directions[(self.snake.snake_direction+1)%4]
        
        
        front_left = center + size * front + size*left
        #print(top_left)
       
        
        for row in range(2*size+1):
            xy = front_left - row * front
            for box in range(2*size+1):
                #print(xy.copy())
                inputDataPositions.append(xy.copy())
                xy -= left
        
        
        
        #print(top_left)
        #print(inputDataPositions)
        #input("Press Enter to continue...")
        
        for element in inputDataPositions:
            x = element[0]
            y = element[1]
            if x<0 or x > number_of_rows-1 or y<0 or y>number_of_columns-1:
                inputDataValues.append(1)
            else:
                inputDataValues.append(self.game_field[x][y])
        
        #print( tuple(np.divide(inputDataValues,3)))
        return tuple(np.divide(inputDataValues,2))
              
            
        
        
    def draw_item(self):
        for item in self.items:
            self.game_field[item.position[0]][item.position[1]]=item.color
        
    def draw_game_field(self,screen):
        pygame.draw.line(screen,index_tuple[1],(game_field_x0,game_field_y0),(game_field_x1,game_field_y0),2)
        pygame.draw.line(screen,index_tuple[1],(game_field_x1,game_field_y0),(game_field_x1,game_field_y1),2)
        pygame.draw.line(screen,index_tuple[1],(game_field_x1,game_field_y1),(game_field_x0,game_field_y1),2)
        pygame.draw.line(screen,index_tuple[1],(game_field_x0,game_field_y1),(game_field_x0,game_field_y0),2)
        
        Score = font.render("Score: "+str(self.score),True,font_color)
        Killer = font.render("Dead in: "+ str(int(kill_timer-self.timer)),True,font_color)
        
        
        screen.blit(Score,Score_rect)
        screen.blit(Killer,Killer_rect)
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
        self.snake_direction = random.choice([0,1,2,3]) # starting index in the directions_list
        self.snake_position = np.array((5, 5))+ np.array((random.randint(0,number_of_rows-10),random.randint(0,number_of_columns-10))) # starting position of the snake head as array so we can use vector additions later
        self.snake_body_color = color_index[color_body] # color of the snake_body is standart white, but could be changed by calling Snake object with extra string arguments
        self.snake_body = [] # empty list where the previous positions of the head and therefor the body is stored
        self.dead = False
        self.frames_per_movement = 10
        
    def move(self,time,game_field,items):
        # only moves snake head every 20 timesteps. Could definitly use a better solution here!
        item_found = False
       
        #creates copy of snake_positions 
        old = self.snake_position.copy()
        
        
        
        #changes snake_position depending to the current direction(vector addition)
        self.snake_position += directions[self.snake_direction]
        
        #check for collisions
        item_found,coll,index = self.collision(items)
        
        self.snake_body.append(old)
            
        #draws snake head reagardless of if it moved or not
        game_field[self.snake_position[0]][self.snake_position[1]]=self.snake_color
            
        return game_field,item_found,coll,index


    
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
    
    def collision(self,items):
        x = self.snake_position[0]
        y = self.snake_position[1]
        index = -1
        item_found = False
        coll = False
        #check for collision with itself
        for bodypart in self.snake_body:
            bodypart_x = bodypart[0]
            bodypart_y = bodypart[1]
            
            if x==bodypart_x and y == bodypart_y:
                #print("collision with self")
                self.dead = True
                coll = True
                return item_found,coll,index
        
        #check for collision with wall
        
        
        if x<0 or x>number_of_rows-2 or y<0 or y>number_of_columns-2:
            self.dead = True
            #print("collision with wall")
            coll = True
            return item_found,coll,index
         
        
        #check for collection of item
        for item in items:
            if np.array_equal(self.snake_position,item.position):
                self.snake_length +=3
                item_found = True
                self.frames_per_movement -=1
                if self.frames_per_movement <1:
                    self.frames_per_movement=1
                index = items.index(item)
            
        return item_found,coll,index



gen = 0
start = (0,0,0)
t_max_per_gen= 1000




def eval_genomes(genomes,config):
    
    global gen
    gen += 1
    run = True
    players = []
    nets = []
    ge =[]
    time = 0
    
    for genome_id, genome in genomes:
        genome.fitness = 0  # start with fitness level of 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        players.append(Game())
        ge.append(genome)
        
    while run and len(players)>0:
        
        time += 1
        screen.fill((0,0,0))
        
        Gen = font.render("Generation: "+ str(gen),True,font_color)
        Alive = font.render("Alive: "+str(len(players)),True,font_color)
        screen.blit(Gen,Gen_rect)
        screen.blit(Alive,Alive_rect)
        
        
        for event in pygame.event.get(): # collects all user input events and iterates through them
            if event.type == pygame.QUIT: # exits game when mouse clicking exit
                run = False
                pygame.quit()
                quit()
                break
        
        for x,player in enumerate(players):
           
            ge[x].fitness += 1/25
            #genarate inputData for each player
            
            if x==0:
                item_found,coll,inputData = player.play(screen,True)
            else:
                item_found,coll,inputData = player.play(screen)
            
            if item_found:
                ge[x].fitness +=10
                
            
            
            
            #print(len(inputData))
            outputData = nets[players.index(player)].activate((inputData))
            #print(outputData)
            # use outputData as action of each player
            if outputData[0]>0.5:
                # changes direction by subtracting 1 from it. using "%4" to make 4 = 0 
                player.snake.snake_direction = (player.snake.snake_direction -1)%4
            elif outputData[1]>0.5:
                player.snake.snake_direction = (player.snake.snake_direction +1)%4
            else:
                ge[x].fitness -=1/50
            
            if coll:
                ge[x].fitness -=5
                
                nets.pop(players.index(player))
                ge.pop(players.index(player))
                players.pop(players.index(player)) 
                
                
           
                
            # implement game mechanics
    
            # increase fitness of player x with:
            # ge[x].fitness += 1 
            
            
            # remove/kill player x with:
            # nets.pop(players.index(player))
            # ge.pop(players.index(player))
            # arms.pop(players.index(player))
            
        # end current genaration after all players have died with:
        
            
def run(config_file):
    """
    runs the NEAT algorithm to train a neural network to play flappy bird.
    :param config_file: location of config file
    :return: None
    """
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(5))

    # Run for up to 5000 generations.
    winner = p.run(eval_genomes, 5000)

    # show final stats
    print('\nBest genome:\n{!s}'.format(winner))


if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    run(config_path)    