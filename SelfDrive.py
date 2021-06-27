import math
import random
import sys
import os
from neat.population import Population

#Pygame module is used to visualize the game
import pygame
#N.E.A.T(NeuroEvolution of Augmenting Topologies), module is used for the ai to find out the right method to complete the track
import neat

#Width and Height is set to the map defaults (Change only if you are adding a new map)
WIDTH = 1697
HEIGHT = 989

#Size of car in pixels (Change only if you changed the map size)
CAR_SIZE_X = 20
CAR_SIZE_Y = 20

#Allows the car to detect crashes outside the map. (Don't change)
BORDER_COLOR = (255, 255, 255, 255)

#Generation counter
current_generation = 0

class Car:

    def __init__(self):
        
        # Loads Car Sprite and Rotates to start position
        self.sprite = pygame.image.load('car.png').convert() # Convert Speeds Up A Lot
        self.sprite = pygame.transform.scale(self.sprite, (CAR_SIZE_X, CAR_SIZE_Y))
        self.rotated_sprite = self.sprite 
        
        #Starting position of the car (in pixel count) (change only if you added a new map)
        self.position = [500, 520]
        self.angle = 0
        self.speed = 0

        #Flag for default speed
        self.speed_set = False 
        
        #Centers the car
        self.center = [self.position[0] + CAR_SIZE_X / 2, self.position[1] + CAR_SIZE_Y / 2]

        #Defines lists to draws radars around the car
        self.radars = []
        self.drawing_radars = []

        #Bool to check if the car is alive or it has crashed
        self.alive = True

        #Sets distance driven and time driven to 0 before starting
        self.distance = 0
        self.time = 0

    #Function to draw the sprite(car) and the radars around it
    def draw(self, screen):
        screen.blit(self.rotated_sprite, self.position) # Draw Sprite
        self.draw_radar(screen) #OPTIONAL FOR SENSORS

    #Function on how to draw the radars
    def draw_radar(self, screen):
        for radar in self.radars:
            position = radar[0]
            #Draws a line from the car and ends in a circle
            pygame.draw.line(screen, (0, 200, 0), self.center, position, 1)
            pygame.draw.circle(screen, (0, 200, 0), position, 5)

    #Function to check if the car has crashed
    def check_collision(self, game_map):
        self.alive = True
        for point in self.corners:
            #If the any corner of the car rouches the border color, it registers it as a crash
            if game_map.get_at((int(point[0]), int(point[1]))) == BORDER_COLOR:
                self.alive = False
                break

    #Function to check the radar
    def check_radar(self, degree, game_map):
        length = 0
        x = int(self.center[0] + math.cos(math.radians(360 - (self.angle + degree))) * length)
        y = int(self.center[1] + math.sin(math.radians(360 - (self.angle + degree))) * length)

        #Keeping going until it hits border color
        while not game_map.get_at((x, y)) == BORDER_COLOR and length < 300:
            length = length + 1
            x = int(self.center[0] + math.cos(math.radians(360 - (self.angle + degree))) * length)
            y = int(self.center[1] + math.sin(math.radians(360 - (self.angle + degree))) * length)

        #Calculate distance to border and append to the radar list
        dist = int(math.sqrt(math.pow(x - self.center[0], 2) + math.pow(y - self.center[1], 2)))
        self.radars.append([(x, y), dist])
    
    #Function to update the map and car speed
    def update(self, game_map):
        if not self.speed_set:
            self.speed = 20
            self.speed_set = True

        #Rotates sprite to move in the x direction and doesnt let car go closer then 20 pixels to the edge 
        self.rotated_sprite = self.rotate_center(self.sprite, self.angle)
        self.position[0] += math.cos(math.radians(360 - self.angle)) * self.speed
        self.position[0] = max(self.position[0], 20)
        self.position[0] = min(self.position[0], WIDTH - 120)

        #Increases distance and time
        self.distance += self.speed
        self.time += 1
        
        ##Rotates sprite to move in the y direction and doesnt let car go closer then 20 pixels to the edge 
        self.position[1] += math.sin(math.radians(360 - self.angle)) * self.speed
        self.position[1] = max(self.position[1], 20)
        self.position[1] = min(self.position[1], WIDTH - 120)

        #Recalculates the center
        self.center = [int(self.position[0]) + CAR_SIZE_X / 2, int(self.position[1]) + CAR_SIZE_Y / 2]

        #Calculates the corners of the map
        length = 0.5 * CAR_SIZE_X
        left_top = [self.center[0] + math.cos(math.radians(360 - (self.angle + 30))) * length, self.center[1] + math.sin(math.radians(360 - (self.angle + 30))) * length]
        right_top = [self.center[0] + math.cos(math.radians(360 - (self.angle + 150))) * length, self.center[1] + math.sin(math.radians(360 - (self.angle + 150))) * length]
        left_bottom = [self.center[0] + math.cos(math.radians(360 - (self.angle + 210))) * length, self.center[1] + math.sin(math.radians(360 - (self.angle + 210))) * length]
        right_bottom = [self.center[0] + math.cos(math.radians(360 - (self.angle + 330))) * length, self.center[1] + math.sin(math.radians(360 - (self.angle + 330))) * length]
        self.corners = [left_top, right_top, left_bottom, right_bottom]

        #Checks for collisions and clears radar if true
        self.check_collision(game_map)
        self.radars.clear()

        #Checks radar from -90 to 120 with step size of 45 
        for d in range(-90, 120, 45):
            self.check_radar(d, game_map)

    #Function to get the radar data
    def get_data(self):
        #Get distance to border
        radars = self.radars
        return_values = [0, 0, 0, 0, 0]
        for i, radar in enumerate(radars):
            return_values[i] = int(radar[1] / 30)

        return return_values

    #Basic alive funtion to check if the car is alive
    def is_alive(self):
        return self.alive

    #Reward funution for the AI to imporve over time
    def get_reward(self):
        return self.distance / (CAR_SIZE_X / 2)

    #Rotates center
    def rotate_center(self, image, angle):
        # Rotate The Rectangle
        rectangle = image.get_rect()
        rotated_image = pygame.transform.rotate(image, angle)
        rotated_rectangle = rectangle.copy()
        rotated_rectangle.center = rotated_image.get_rect().center
        rotated_image = rotated_image.subsurface(rotated_rectangle).copy()
        return rotated_image


def run_simulation(genomes, config):
    
    #Empty list for nets and cars
    nets = []
    cars = []

    #Initiates pygame and its display
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)

    #Creates new neural network for all genomes passed
    for i, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        g.fitness = 0

        cars.append(Car())

    #Clock, font, and map settings
    clock = pygame.time.Clock()
    generation_font = pygame.font.SysFont("Arial", 30)
    alive_font = pygame.font.SysFont("Arial", 20)
    game_map = pygame.image.load('map2.png').convert() # Convert Speeds Up A Lot

    #Defines variable generation
    global current_generation
    current_generation += 1

    #Counter to limit time
    counter = 0

    #Exits game on quit
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)

        #Get the action of each car
        for i, car in enumerate(cars):
            output = nets[i].activate(car.get_data())
            choice = output.index(max(output))
            if choice == 0:
                car.angle += 10 #Left
            elif choice == 1:
                car.angle -= 10 #Right
            elif choice == 2:
                if(car.speed - 2 >= 12):
                    car.speed -= 2 #Slow down
            else:
                car.speed += 2 #Speed up
        
        #Check if car is alive and increase fitness accordingly, else break
        still_alive = 0
        for i, car in enumerate(cars):
            if car.is_alive():
                still_alive += 1
                car.update(game_map)
                genomes[i][1].fitness += car.get_reward()

        if still_alive == 0:
            break

        #Stop after 20 seconds of breaking
        counter += 1
        if counter == 30 * 40:
            break

        #Draws map and alive cars
        screen.blit(game_map, (0, 0))
        for car in cars:
            if car.is_alive():
                car.draw(screen)
        
        #Prints generation count and number of cars alive
        text = generation_font.render("Generation: " + str(current_generation), True, (0,0,0))
        text_rect = text.get_rect()
        text_rect.center = (200, 650)
        screen.blit(text, text_rect)
        text = alive_font.render("Still Alive This Generation: " + str(still_alive), True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (200, 690)
        screen.blit(text, text_rect)
        text = alive_font.render("Total Death Count: " + str((current_generation * int(config.pop_size)) - still_alive), True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (200, 730)
        screen.blit(text, text_rect)
        
        #Sets fps to 60
        pygame.display.flip()
        clock.tick(60)
        
if __name__ == "__main__":
    
    #Loads config from config.txt
    config_path = "./config.txt"
    config = neat.config.Config(neat.DefaultGenome,
                                neat.DefaultReproduction,
                                neat.DefaultSpeciesSet,
                                neat.DefaultStagnation,
                                config_path)

    #Creeates population and reports
    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)
    
    #Runs simulation with max generations set to 10000
    population.run(run_simulation, 10000)
    print("e")
