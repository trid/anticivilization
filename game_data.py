import pickle
import time
import math
import random
from building_manager import BuildingManager
import expedition
from game_map import GameMap
import game_map
from map_gen.river_gen import generate_rivers
from monster import Monster
from point import Point
from specialist import Specialist
import specialist
from village import Village

__author__ = 'TriD'


class GameData():
    def place_resources(self):
        #And, yes, that's a really bad code.
        #TODO: Find some time to change it totally
        for i in range(0, 100):
            tile = self.game_map[random.randint(0, game_map.MAP_WIDTH * game_map.SQUARE_WIDTH)][
                random.randint(0, game_map.MAP_HEIGHT * game_map.SQUARE_HEIGHT)]
            if tile.ground != 'water':
                tile.resource = 'tree'
            tile = self.game_map[random.randint(0, game_map.MAP_WIDTH * game_map.SQUARE_WIDTH)][
                random.randint(0, game_map.MAP_HEIGHT * game_map.SQUARE_HEIGHT)]
            if tile.ground != 'water':
                tile.resource = 'stone'
            tile = self.game_map[random.randint(0, game_map.MAP_WIDTH * game_map.SQUARE_WIDTH)][
                random.randint(0, game_map.MAP_HEIGHT * game_map.SQUARE_HEIGHT)]
            if tile.ground != 'water':
                tile.resource = 'iron'

    def place_center(self):
        self.center = Point(5, 5)
        while self.game_map[self.center.x][self.center.y].ground == 'water':
            self.center.x += 1
            self.center.y += 1
        self.game_map[self.center.x][self.center.y].building = 'center'

    def place_monsters(self):
        self.monsters = []
        for i in range(0, 30):
            monster = Monster(self.game_map)
            monster.x = random.randint(0, game_map.MAP_WIDTH * game_map.SQUARE_WIDTH)
            monster.y = random.randint(0, game_map.MAP_HEIGHT * game_map.SQUARE_HEIGHT)
            monster.level = int(math.sqrt((self.center.x - monster.x) ** 2 + (self.center.y - monster.y) ** 2) / 50) + 1
            self.monsters.append(monster)
            self.game_map[monster.x][monster.y].units.append(monster)

    def __init__(self):
        self.drag = False
        self.done = False
        self.game_map = GameMap()
        generate_rivers(self.game_map)
        self.place_center()
        self.place_resources()
        self.old_dx = 0
        self.old_dy = 0
        self.dx = -(300 - 32 * self.center.x)
        self.dy = -(300 - 32 * self.center.y)
        self.scroll_spd_x, self.scroll_spd_y = 0, 0
        self.exp_pos = None
        self.village = Village()
        self.expeditions = []
        self.turn = 0
        self.place_monsters()
        self.specialists = [Specialist(specialist.CHIEFTAIN)]
        self.last_time = time.time() * 1000
        self.accum = 0

    def send_expedition(self):
        self.uis.show_chose_specialists_dialog()

    def destroy_expedition(self, monster_tile, exp):
        exp.status = expedition.DEAD
        for spec in exp.warriors + exp.workers:
            self.specialists.remove(spec)
        self.village.population -= exp.people
        monster_tile.units.remove(exp)

    def move_monsters(self):
        for monster in self.monsters:
            self.game_map[monster.x][monster.y].units.remove(monster)
            monster.move()

            monster_tile = self.game_map[monster.x][monster.y]
            for unit in monster_tile.units:
                if isinstance(unit, expedition.Expedition):
                    if self.process_battle(monster, expedition) == monster:
                        self.destroy_expedition(monster_tile, unit)
                    else:
                        self.destroy_monster(monster)
                        for specialist in unit.warriors:
                            specialist.add_exp(monster.level * 100)
            if monster_tile.building:
                self.village.remove_building(monster_tile.building)
                monster_tile.building = None
            if monster.alive:
                monster_tile.units.append(monster)

    def move_expeditions(self):
        for expedition_item in self.expeditions:
            self.game_map[expedition_item.x][expedition_item.y].units.remove(expedition_item)
            expedition_item.make_move()
            tile = self.game_map[expedition_item.x][expedition_item.y]
            for unit in tile.units:
                if type(unit) == Monster:
                    if self.process_battle(unit, expedition) == unit:
                        self.destroy_expedition(tile, unit)
                    else:
                        self.destroy_monster(unit)
                        tile.units.remove(unit)
                        for specialist in expedition.warriors:
                            specialist.add_exp(unit.level * 100)
            if expedition_item.status == expedition.FINISHED:
                self.village.change_resource_count(expedition_item.resource, expedition_item.get_resources_count())
            else:
                tile.units.append(expedition_item)
        self.expeditions = filter(lambda x: x.status != expedition.FINISHED and x.status != expedition.DEAD,
                                  self.expeditions)

    def next_turn(self):
        self.turn += 1
        self.village.update()
        self.move_monsters()
        self.move_expeditions()

    def build(self, mouse_x, mouse_y):
        if not self.uis.building:
            return

        x = (self.dx + mouse_x) / 32
        y = (self.dy + mouse_y) / 32

        may_build = False
        if self.game_map[x][y].building:
            if self.uis.building == 'destruct' and self.uis.building != 'center':
                building = self.game_map[x][y].building
                finished = self.game_map[x][y].building_finished
                if finished:
                    self.game_map[x][y].building_finished = False
                    self.village.remove_building(building)
                    self.village.to_build.remove(building)
                self.game_map[x][y].building = None
            return
        if self.game_map[x][y].ground == 'water':
            return

        if self.game_map[x - 1][y].building:
            may_build = True
        if self.game_map[x - 1][y - 1].building:
            may_build = True
        if self.game_map[x - 1][y - 1].building:
            may_build = True
        if self.game_map[x][y - 1].building:
            may_build = True
        if self.game_map[x + 1][y - 1].building:
            may_build = True
        if self.game_map[x + 1][y].building:
            may_build = True
        if self.game_map[x + 1][y + 1].building:
            may_build = True
        if self.game_map[x][y + 1].building:
            may_build = True
        if may_build:
            self.set_building(x, y)

    def set_building(self, x, y):
        bm = BuildingManager()
        bc = bm.conds[self.uis.building]
        for resource in bc.resources:
            amount = self.village.get_resource_count(resource)
            if amount < bc.resources[resource]:
                return

        tile = self.game_map[x][y]
        for cond in bc.tile_params:
            if cond != tile.resource:
                return

        if not self.check_nearby_tiles(x, y, bc.near):
            return

        for resource in bc.resources:
            self.village.change_resource_count(resource, -bc.resources[resource])

        tile.building = self.uis.building
        tile.building_finished = False
        self.village.add_building(self.uis.building, tile)

    def check_nearby_tiles(self, x, y, cond):
        """Conditions for nearby tiles. Specially for port building"""
        points = (self.game_map[x][y - 1],
                  self.game_map[x + 1][y - 1],
                  self.game_map[x + 1][y],
                  self.game_map[x + 1][y + 1],
                  self.game_map[x][y + 1],
                  self.game_map[x - 1][y + 1],
                  self.game_map[x - 1][y],
                  self.game_map[x - 1][y - 1])
        for param in cond:
            result = False
            for point in points:
                result = getattr(point, param) == cond[param] or result
            if not result:
                return False
        return True

    def process_battle(self, monster, expedition):
        monster_power = monster.level * 100
        exp_power = 0
        for specialist in expedition.warriors:
            exp_power += specialist.level
        exp_power *= expedition.people
        if monster_power > exp_power:
            return monster
        return expedition

    def process(self):
        curr_time = time.time() * 1000
        delta = curr_time - self.last_time
        self.last_time = curr_time
        self.accum += delta

        if self.accum >= 100:
            self.accum -= 100
            self.dx += self.scroll_spd_x
            self.dy += self.scroll_spd_y

    def destroy_monster(self, monster):
        monster.alive = False
        self.monsters.remove(monster)
