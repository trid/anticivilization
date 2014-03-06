from expedition import Expedition
import expedition
from pathfinder import AStarFinder
from point import Point

__author__ = 'TriD'

import random


class Monster:
    def __init__(self, game_map):
        self.x = 0
        self.y = 0
        self.speed = 2
        self.environment = 'ground'
        self.level = 1
        self.view_radius = 5
        self.target = None
        self.path = None
        self.game_map = game_map

    def random_move(self):
        self.x += random.randint(-1, 1)
        self.y += random.randint(-1, 1)

    def reset_path(self, game_map):
        self.path = AStarFinder().find(game_map, Point(self.x, self.y), Point(self.target.x, self.target.y))

    def search(self, game_map):
        for x in range(self.x - self.view_radius, self.x + self.view_radius):
            for y in range(self.y - self.view_radius, self.y + self.view_radius):
                for unit in game_map[x][y].units:
                    if isinstance(unit, Expedition):
                        self.target = game_map[x][y].unit
                        self.reset_path(game_map)
                        return True
        return False

    def move(self):
        if self.target:
            if abs(self.x - self.target.x) < 5 and abs(self.y - self.y) < 5 and (self.target.status != expedition.DEAD and self.target.status != expedition.FINISHED):
                self.reset_path(self.game_map)
                self.path.pop()
                node = self.path.pop()
                self.x, self.y = node.x, node.y
            else:
                self.target = None
                self.path = None
                self.random_move()
        else:
            if self.search(self.game_map):
                self.move()
                return
            self.random_move()
