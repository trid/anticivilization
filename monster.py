from expedition import Expedition
import expedition
from ai.pathfinder import AStarFinder
from point import Point
import random


ENV_GROUND = 0
ENV_AQUATIC = 1
ENV_AMPHIBIOUS = 2


class Monster:
    def __init__(self, game_map):
        self.x = 0
        self.y = 0
        self.speed = 2
        self.environment = ENV_GROUND
        self.level = 1
        self.view_radius = 5
        self.target = None
        self.path = None
        self.game_map = game_map
        self.alive = True

    def random_move(self):
        if random.randint(0, 1):
            x = self.x + random.randint(-1, 1)
            y = self.y
        else:
            x = self.x
            y = self.y + random.randint(-1, 1)
        self.x = x
        self.y = y

    def reset_path(self):
        self.path = AStarFinder().find(self.game_map, Point(self.x, self.y), Point(self.target.x, self.target.y))

    def search(self, game_map):
        for x in range(self.x - self.view_radius, self.x + self.view_radius):
            for y in range(self.y - self.view_radius, self.y + self.view_radius):
                for unit in game_map[x][y].units:
                    if isinstance(unit, Expedition):
                        self.target = unit
                        self.reset_path()
                        return True
        return False

    def move(self):
        if self.target:
            if abs(self.x - self.target.x) < 5 and abs(self.y - self.y) < 5 and (self.target.status != expedition.DEAD and self.target.status != expedition.FINISHED):
                self.reset_path()
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
