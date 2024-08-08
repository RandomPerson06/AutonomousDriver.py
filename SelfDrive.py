import math
import sys
import pygame
import neat
import pygame_gui
import matplotlib.pyplot as plt
import threading

# Global variables
ShowRadar = True
racemap = 2

WIDTH = 1697
HEIGHT = 989

CAR_SIZE_X = 20
CAR_SIZE_Y = 20

BORDER_COLOR = (255, 255, 255, 255)

current_generation = 0
fitness_scores = []

class Car:
    def __init__(self):
        # Initialize car properties
        self.sprite = pygame.image.load('car.png').convert()
        self.sprite = pygame.transform.scale(self.sprite, (CAR_SIZE_X, CAR_SIZE_Y))
        self.rotated_sprite = self.sprite
        self.position = [500, 520]
        self.angle = 0
        self.speed = 20
        self.center = [self.position[0] + CAR_SIZE_X / 2, self.position[1] + CAR_SIZE_Y / 2]
        self.radars = []
        self.alive = True
        self.distance = 0
        self.time = 0

    def draw(self, screen):
        # Draw the car on the screen
        screen.blit(self.rotated_sprite, self.position)
        if ShowRadar:
            self.draw_radar(screen)

    def draw_radar(self, screen):
        # Draw the radar lines and circles
        for radar in self.radars:
            position = radar[0]
            pygame.draw.line(screen, (0, 200, 0), self.center, position, 1)
            pygame.draw.circle(screen, (0, 200, 0), position, 5)

    def check_collision(self, game_map):
        # Check for collision with the border
        for point in self.corners:
            if game_map.get_at((int(point[0]), int(point[1]))) == BORDER_COLOR:
                self.alive = False
                break

    def check_radar(self, degree, game_map):
        # Check the radar distance
        length = 0
        x = int(self.center[0] + math.cos(math.radians(360 - (self.angle + degree))) * length)
        y = int(self.center[1] + math.sin(math.radians(360 - (self.angle + degree))) * length)

        while not game_map.get_at((x, y)) == BORDER_COLOR and length < 300:
            length += 1
            x = int(self.center[0] + math.cos(math.radians(360 - (self.angle + degree))) * length)
            y = int(self.center[1] + math.sin(math.radians(360 - (self.angle + degree))) * length)

        dist = int(math.sqrt((x - self.center[0]) ** 2 + (y - self.center[1]) ** 2))
        self.radars.append([(x, y), dist])

    def update(self, game_map):
        # Update the car's position and check for collisions
        self.rotated_sprite, rotated_rect = self.rotate_center(self.sprite, self.angle)
        self.position[0] += math.cos(math.radians(360 - self.angle)) * self.speed
        self.position[0] = max(20, min(self.position[0], WIDTH - 120))
        self.distance += self.speed
        self.time += 1
        self.position[1] += math.sin(math.radians(360 - self.angle)) * self.speed
        self.position[1] = max(20, min(self.position[1], HEIGHT - 120))
        self.center = [int(self.position[0]) + CAR_SIZE_X / 2, int(self.position[1]) + CAR_SIZE_Y / 2]

        length = 0.5 * CAR_SIZE_X
        angles = [30, 150, 210, 330]
        self.corners = [
            [self.center[0] + math.cos(math.radians(360 - (self.angle + a))) * length,
             self.center[1] + math.sin(math.radians(360 - (self.angle + a))) * length]
            for a in angles
        ]

        self.check_collision(game_map)
        self.radars.clear()
        for d in range(-90, 120, 45):
            self.check_radar(d, game_map)

    def get_data(self):
        # Get radar data
        return [int(radar[1] / 30) for radar in self.radars]

    def is_alive(self):
        # Check if the car is still alive
        return self.alive

    def get_reward(self):
        # Calculate the reward based on distance traveled
        return self.distance / (CAR_SIZE_X / 2)

    def rotate_center(self, image, angle):
        # Rotate the image around its center
        rotated_image = pygame.transform.rotate(image, angle)
        rotated_rect = rotated_image.get_rect(center=image.get_rect(center=(self.position[0] + CAR_SIZE_X / 2, self.position[1] + CAR_SIZE_Y / 2)).center)
        return rotated_image, rotated_rect

def run_simulation(genomes, config, screen, clock, manager):
    # Run the simulation for each generation
    nets = []
    cars = []

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        g.fitness = 0
        cars.append(Car())

    generation_font = pygame.font.SysFont("Arial", 30)
    alive_font = pygame.font.SysFont("Arial", 20)
    game_map = pygame.image.load(f'map{racemap}.png').convert()

    global current_generation
    current_generation += 1

    counter = 0

    while True:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            manager.process_events(event)

        still_alive = 0
        for i, car in enumerate(cars):
            if car.is_alive():
                still_alive += 1
                car.update(game_map)
                genomes[i][1].fitness += car.get_reward()
                output = nets[i].activate(car.get_data())
                choice = output.index(max(output))
                if choice == 0:
                    car.angle += 10
                elif choice == 1:
                    car.angle -= 10
                elif choice == 2 and car.speed - 2 >= 12:
                    car.speed -= 2
                else:
                    car.speed += 2

        if still_alive == 0 or counter == 30 * 40:
            break

        screen.blit(game_map, (0, 0))
        for car in cars:
            if car.is_alive():
                car.draw(screen)

        text = generation_font.render(f"Generation: {current_generation}", True, (0, 0, 0))
        screen.blit(text, (200, 650))
        text = alive_font.render(f"Still Alive This Generation: {still_alive}", True, (0, 0, 0))
        screen.blit(text, (200, 690))
        text = alive_font.render(f"Total Death Count: {(current_generation * int(config.pop_size)) - still_alive}", True, (0, 0, 0))
        screen.blit(text, (200, 730))

        manager.update(time_delta)
        manager.draw_ui(screen)

        pygame.display.flip()
        counter += 1

    fitness_scores.append(sum([g.fitness for _, g in genomes]) / len(genomes))

def plot_fitness():
    # Plot the fitness scores over generations
    plt.ion()
    fig, ax = plt.subplots()
    while True:
        ax.clear()
        ax.plot(fitness_scores)
        ax.set_xlabel('Generation')
        ax.set_ylabel('Average Fitness')
        ax.set_title('Fitness over Generations')
        plt.pause(1)

if __name__ == "__main__":
    # Main function to initialize and run the simulation
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    clock = pygame.time.Clock()
    manager = pygame_gui.UIManager((WIDTH, HEIGHT))

    config_path = "config.txt"
    config = neat.config.Config(neat.DefaultGenome,
                                neat.DefaultReproduction,
                                neat.DefaultSpeciesSet,
                                neat.DefaultStagnation,
                                config_path)

    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    plot_thread = threading.Thread(target=plot_fitness)
    plot_thread.daemon = True
    plot_thread.start()

    population.run(lambda genomes, config: run_simulation(genomes, config, screen, clock, manager), 99999999)