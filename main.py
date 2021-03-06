import os.path

import pygame
import random
import math
import csv
import pandas as pd
import tkinter as tk

from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000


def find_home():  # This function randomly selects a location on the edge of the environment to place a creature and
    # have that spot designated as the creatures home location
    home = (0, 0)
    side = random.randint(0, 3)
    if side == 0:
        home = (random.randint(5, SCREEN_WIDTH - 5), 5)
    elif side == 1:
        home = (SCREEN_WIDTH - 5, random.randint(0, SCREEN_HEIGHT - 5))
    elif side == 2:
        home = (random.randint(5, SCREEN_WIDTH - 5), SCREEN_HEIGHT - 5)
    elif side == 3:
        home = (5, random.randint(5, SCREEN_HEIGHT - 5))

    return home


def create_child(stats):  # This function creates a new creature and adds it to the creatures and all_sprites groups
    new_creature = Creature(stats)
    creatures.add(new_creature)
    all_sprites.add(new_creature)


def randomize_stats(a):  # This function randomly selects a number 1 smaller, 1 larger, or the same as the number
    # passed in
    b = random.randint(-1, 1)
    return a + b


class Creature(pygame.sprite.Sprite):
    def __init__(self, stats):
        self.my_stats = stats.copy()
        for x in self.my_stats:
            self.my_stats[x] = randomize_stats(self.my_stats[x])
        super(Creature, self).__init__()
        self.speed = self.my_stats["base_speed"]
        self.size = self.my_stats["base_size"]
        self.max_energy = self.my_stats["creature_energy"]
        self.energy = self.max_energy
        self.surf = pygame.Surface((self.size * 4, self.size * 4))
        self.surf.fill((random.randint(0, 200), random.randint(0, 200), random.randint(0, 200)))
        self.rect = self.surf.get_rect()

        self.num_food_eaten = 0
        self.home = find_home()
        self.rect.center = self.home
        self.at_home = True
        self.rounds_to_live = 5
        self.destination = 0

    def eat_creature(self):  # This functions simply adds 5 to a creatures current food count. This happens when a
        # creature eats another creature
        self.num_food_eaten = self.num_food_eaten + 5

    def end_of_round(self):  # This function takes care of several things that need to happen to each creature at the
        # end of each round
        self.rounds_to_live -= 1
        self.energy = self.max_energy
        if self.num_food_eaten > 6:
            create_child(self.my_stats)
        self.num_food_eaten = 0

    def is_at_home(self):  # This is a getter function for the variable at_home
        if self.at_home is True:
            return True
        else:
            return False

    def eat_food(self):  # This function adds 1 to the number of food a creature is eaten
        self.num_food_eaten = self.num_food_eaten + 1

    def find_closest_food(self, foods):  # This function returns the food object that is currently the closest to
        # that creature
        current_smallest = 10000000
        close_food = None
        for food in foods:
            p1 = self.rect.center
            p2 = food.rect.center
            distance = math.sqrt(((p1[0] - p2[0]) ** 2) + ((p1[1] - p2[1]) ** 2))

            if distance < current_smallest:
                current_smallest = distance
                close_food = food
                if distance < self.speed:
                    self.rect.centerx = close_food.rect.centerx
                    self.rect.centery = close_food.rect.centery
        return close_food

    def get_direction(self, x, y):  # This function returns the direction that a creature should move based on the
        # coordinates of its destination that are passed in
        direction_x = 0
        direction_y = 0
        if self.rect.centerx < x:
            direction_x = self.speed
        if self.rect.centerx > x:
            direction_x = -self.speed
        if self.rect.centery < y:
            direction_y = self.speed
        if self.rect.centery > y:
            direction_y = -self.speed

        direction = (direction_x, direction_y)
        return direction

    def update(self, foods):  # This is the main function that is called each time a creature needs to move. It
        # handles everything that should happen
        if self.destination == 0:
            closest_food = self.find_closest_food(foods)

            direction = self.get_direction(closest_food.rect.centerx, closest_food.rect.centery)
        elif self.destination == 1:
            direction = self.get_direction(self.home[0], self.home[1])
            p1 = self.home
            p2 = self.rect.center
            home_distance = math.sqrt(((p1[0] - p2[0]) ** 2) + ((p1[1] - p2[1]) ** 2))

            if home_distance < self.speed:
                self.rect.centerx = self.home[0]
                self.rect.centery = self.home[1]

        if self.rect.center == self.home:
            self.at_home = True
        else:
            self.at_home = False

        self.rect.move_ip(direction)
        if self.speed < 1:
            self.energy = 1
        self.energy -= (self.speed ** 2) + (self.size ** 3)
        if self.energy <= 0:
            self.destination = 1


class Food(pygame.sprite.Sprite):
    def __init__(self):
        super(Food, self).__init__()
        self.surf = pygame.Surface((20, 20))
        self.surf.fill((255, 0, 255))
        self.rect = self.surf.get_rect()
        self.rect.center = (
            random.randint(0, SCREEN_WIDTH),
            random.randint(0, SCREEN_HEIGHT),
        )


simulation_stats = {
    "num_foods": 200,
    "num_creatures": 4,
    "creature_energy": 50000,
    "base_speed": 3,
    "base_size": 3
}


def apply():
    simulation_stats[0] = int(e1.get())
    simulation_stats[1] = int(e2.get())
    simulation_stats[2] = int(e3.get())
    simulation_stats[3] = int(e4.get())
    simulation_stats[4] = int(e5.get())


master = tk.Tk()
tk.Label(master, text="Number of Food Objects").grid(row=0)
tk.Label(master, text="Number of Creatures").grid(row=1)
tk.Label(master, text="Creature Energy").grid(row=2)
tk.Label(master, text="Base Creature Speed").grid(row=3)
tk.Label(master, text="Base Creature Size").grid(row=4)

e1 = tk.Entry(master)
e2 = tk.Entry(master)
e3 = tk.Entry(master)
e4 = tk.Entry(master)
e5 = tk.Entry(master)
e1.insert(10, '200')
e2.insert(10, '4')
e3.insert(10, '50000')
e4.insert(10, '3')
e5.insert(10, '3')

e1.grid(row=0, column=1)
e2.grid(row=1, column=1)
e3.grid(row=2, column=1)
e4.grid(row=3, column=1)
e5.grid(row=4, column=1)

tk.Button(master,
          text='Run',
          command=master.quit).grid(row=6,
                                    column=0,
                                    sticky=tk.W,
                                    pady=4)
tk.Button(master, text='Apply', command=apply).grid(row=6,
                                                    column=1,
                                                    sticky=tk.W,
                                                    pady=4)

master.mainloop()

tk.mainloop()

# Stats
environment_stats = {
    "num_foods": simulation_stats[0],
    "num_creatures": simulation_stats[1]
}

creature_stats = {
    "base_speed": simulation_stats[3],
    "base_size": simulation_stats[4],
    "creature_energy": simulation_stats[2]
}

# Start of pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
font = pygame.font.SysFont(None, 24)
clock = pygame.time.Clock()


# create groups
foods = pygame.sprite.Group()
creatures = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

# CSV file opening
filename = "selectiondata.csv"
f = open(filename, "w+")
f.close()

with open('selectiondata.csv', 'a', newline='') as csvfile:
    mywriter = csv.writer(csvfile, delimiter=',', lineterminator='\n')
    mywriter.writerow(('Generation Number', 'Number of Creatures', 'Average Speed', 'Average Size',
                       'Number of Food Objects Remaining'))

# Initialization of necessary variables
generation_count = 1
left_foods = 0
phase = 0
all_creatures_at_home = True
some_creatures_have_energy = True
running = True

# create original creatures
j = 0
while j < environment_stats["num_creatures"]:
    create_child(creature_stats)
    j += 1

while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
                filepath = os.path.dirname(os.path.abspath(__file__))

                read_file = pd.read_csv(filepath + '\selectiondata.csv')
                read_file.to_excel(filepath + '\selectiondata.xlsx', index=None, header=True)
        elif event.type == QUIT:
            running = False
            filepath = os.path.dirname(os.path.abspath(__file__))

            read_file = pd.read_csv(filepath + '\selectiondata.csv')
            read_file.to_excel(filepath + '\selectiondata.xlsx', index=None, header=True)

    screen.fill((255, 255, 255))

    if phase == 0:
        for x in creatures:
            x.destination = 0
        phase = 1
    elif phase == 1:
        i = 0
        while i < environment_stats["num_foods"]:
            new_food = Food()
            foods.add(new_food)
            all_sprites.add(new_food)
            i += 1
        phase = 2
    elif phase == 2:
        creatures.update(foods)

        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)

        dictionary_food = pygame.sprite.groupcollide(creatures, foods, False, False)
        for x in dictionary_food:
            if x.energy > 0:
                x.eat_food()
                dictionary_food[x][0].kill()
        for x in creatures:
            eaten_creature = pygame.sprite.spritecollide(x, creatures, False)
            if len(eaten_creature) > 1:
                ratio = x.size / float(eaten_creature[1].size)
                if eaten_creature[1] is not None and x is not eaten_creature[1] and ratio > 1.2 and x.energy > 0 and \
                        eaten_creature[1].energy > 0:
                    x.eat_creature()
                    eaten_creature[1].kill()
            eaten_creature = None
        if len(foods) <= 0:
            for x in creatures:
                x.destination = 1
            all_creatures_at_home = True
            for x in creatures:
                if x.is_at_home() is False:
                    all_creatures_at_home = False
            if all_creatures_at_home:
                phase = 3
        some_creatures_have_energy = False
        for x in creatures:
            if x.energy >= 0:
                some_creatures_have_energy = True
        num_foods_remaining = 0
        if not some_creatures_have_energy:
            for x in foods:
                x.kill()
                num_foods_remaining += 1
                if num_foods_remaining > 0:
                    left_foods = num_foods_remaining

    elif phase == 3:
        for x in creatures:
            if x.num_food_eaten < 5:
                x.kill()
        for x in creatures:
            x.end_of_round()
            if x.rounds_to_live <= 0:
                x.kill()
        sum = 0
        for x in creatures:
            sum += x.size
        average_size = sum / len(creatures)
        sum = 0
        for x in creatures:
            sum += x.speed
        average_speed = sum / len(creatures)
        with open('selectiondata.csv', 'a', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',', lineterminator='\n')
            spamwriter.writerow((generation_count, len(creatures), average_speed, average_size, left_foods))
            left_foods = 0
        generation_count += 1
        phase = 0

    img = font.render(str(generation_count), True, (0, 0, 0))
    screen.blit(img, (20, 20))
    clock.tick(60)

    pygame.display.flip()
