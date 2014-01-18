from math import sqrt
from ai.pathfinder import AStarFinder
from point import Point
import specialist
from tile_data import tile_data

__author__ = 'TriD'

STARTED = 1
RETURNING = 2
FINISHED = 3
DEAD = 4


class Expedition:
    def __init__(self, specialists, position_from, people):
        self.x = position_from.x
        self.y = position_from.y
        self.center = position_from
        self.status = STARTED
        self.path = []
        self.warriors = []
        self.workers = []
        self.speed = 4
        self.people = 0
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
            tile_on = self.game_map[self.x][self.y]
            ground_on = tile_on.ground
            tile_to_move = self.game_map[point.x][point.y]
            if ground_on == 'water' and tile_to_move.ground == 'grass' and tile_to_move.building is None:
                tile_to_move.building = 'boat'
            if tile_on.building == 'boat' and tile_to_move.ground == 'water':
                tile_on.building = None
            self.x = point.x
            self.y = point.y
            self.path.pop()

    def make_move(self):
        steps_left = self.speed
        while (self.status != DEAD or self.status != FINISHED) and self.can_move(steps_left):
            self.move()
            tile = self.game_map[self.x][self.y]
            movement_cost = 1 if tile.building == 'road' else tile_data[tile.ground]
            steps_left -= movement_cost
            if not self.path:
                if self.status != RETURNING:
                    self.status = RETURNING
                    self.resource = self.game_map[self.x][self.y].resource
                    self.find_path(self.x, self.y, self.center.x, self.center.y, self.game_map)
                else:
                    self.status = FINISHED
                    self.release_specialists()
                    return

    def can_move(self, steps_left):
        position = self.path[-1]
        tile = self.game_map[position.x][position.y]
        movement_cost = 1 if tile.building == 'road' else tile_data[tile.ground]
        return steps_left >= movement_cost

    def release_specialists(self):
        for warrior in self.warriors:
            warrior.occupied = False
        for worker in self.workers:
            worker.occupied = False
