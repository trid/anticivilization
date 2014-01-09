from math import sqrt
from ai.pathfinder import AStarFinder
from point import Point
import specialist

__author__ = 'TriD'

STARTED = 1
RETURNING = 2
FINISHED = 3
DEAD = 4


class Expedition:
    def __init__(self, specialists):
        self.x = 5
        self.y = 5
        self.status = STARTED
        self.path = []
        self.warriors = []
        self.workers = []
        for specialist_instance in specialists:
            specialist_instance.occupied = True
            if specialist_instance.s_type == specialist.WORKER:
                self.workers.append(specialist_instance)
            elif specialist_instance.s_type == specialist.WARRIOR:
                self.warriors.append(specialist_instance)
            else:
                self.workers.append(specialist_instance)
                self.warriors.append(specialist_instance)

    def find_path(self, pos_x, pos_y, dst_x, dst_y, game_map):
        #Here we go with an A*
        #I know it's wrong, but let's just leave it here, hope i'll fix it later, ok?
        self.game_map = game_map
        path = AStarFinder().find(game_map, Point(pos_x, pos_y), Point(dst_x, dst_y))
        self.path = path
        self.path.pop()

    def move(self):
        if self.path:
            point = self.path[-1]
            self.x = point.x
            self.y = point.y
            self.path.pop()
        elif self.status != RETURNING:
            self.status = RETURNING
            self.find_path(self.x, self.y, 5, 5, self.game_map)
            self.x, self.y = (self.path[-1].x, self.path[-1].y)
            self.path.pop()
        else:
            self.status = FINISHED
            self.release_specialists()

    def release_specialists(self):
        for warrior in self.warriors:
            warrior.occupied = False
        for worker in self.workers:
            worker.occupied = False
