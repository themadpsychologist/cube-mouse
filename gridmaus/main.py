'''The game backend.
All addresses, including movement addresses, are tuples.
'''

import math
from random import random

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400

class BuildWorld():
    '''Isn't a world, but prepares to build one'''
    def __init__(self):
        self.dimensions = 2
        self.size = 5

    def change_size(self, _, size):
        '''Called by selector onchange'''
        self.size = size

    def change_dimensions(self, _, dimensions):
        '''Called by selector onchange'''
        self.dimensions = dimensions


class World():
    '''Handles in-game abstractions'''
    def __init__(self, dimensions, size):
        self.dimensions = dimensions
        self.size = size

        dimension_center = int(self.size / 2)
        self.dimension_range = range(dimensions)

        self.goal = self.generate_goal()
        self.player_location = tuple(dimension_center for x in self.dimension_range)

    def generate_goal(self):
        '''Sets the goal at the beginning of the game'''
        return tuple(rand_range(self.size) for x in self.dimension_range)

    def move_player(self, movement):
        '''Pretty much all the controls are hooked here.'''
        results = dict()
        address = move_address(self.player_location, movement, self.size - 1)
        results['velocity'] = get_velocity(self.goal, self.player_location, address)
        if self.player_location == address:
            results['reached_goal'] = True
        else:
            results['reached_goal'] = False
            self.player_location = address
        return results


def adjust_to_boundaries(coordinate, boundary):
    '''Keeps the player from leaving the game area'''
    return boundary if coordinate > boundary else 0 if coordinate < 0 else coordinate

def eat_food():
    '''Victory message'''
    with open('foods.txt', 'r') as foods_file:
        foods = [foods_file]
    food = foods[rand_range(len(foods))]
    food = food.rstrip('\n')
    print(f'The mouse finds {food} and scarfs it down. Good job!')

def game_loop():
    '''The main game loop'''
    game_world = World(build_world.dimensions, build_world.size)
    running = True
    while running:
        move_results = game_world.move_player(
            tuple(rand_range(3) - 1 for x in game_world.dimension_range)
            )
        if move_results['reached_goal']:
            running = False
        else:
            print(move_results['velocity']) # for testing; pipe to display

def generate_numerical_selector(min_size, max_size):
    '''Helper function for Game.showMenu()'''
    return [(str(x), x) for x in range(min_size, max_size + 1)]

def get_difference(int1, int2):
    '''To shorten an unwieldy list comprehension'''
    return abs(int1 - int2)

def get_distance(address1, address2):
    '''In Cartesian space using tuples'''
    distances = tuple(get_difference(address1[x], address2[x]) for x in range(len(address1)))
    totalDistance = math.hypot(*distances)
    return totalDistance

def get_velocity(goal, address1, address2):
    '''The player gets a readout of this.'''
    return get_distance(address1, goal) - get_distance(address2, goal)

def move_address(address, movement, boundary):
    '''Helper function for World.move_player'''
    return tuple(
            adjust_to_boundaries(address[x] + movement[x], boundary)
            for x in movement
            )

def rand_range(maximum):
    '''Supposed to be faster than randrange'''
    return int(random() * maximum)


build_world = BuildWorld()
