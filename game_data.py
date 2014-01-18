import time
from building_manager import BuildingManager
import expedition
from game_map import GameMap
from map_gen.river_gen import generate_rivers
from monster import Monster
from point import Point
from specialist import Specialist
import specialist
from village import Village

__author__ = 'TriD'


class GameData():
    def place_resources(self):
        self.game_map[9][9].resource = 'tree'
        self.game_map[-20][0].resource = 'tree'
        self.game_map[20][0].resource = 'tree'

    def place_center(self):
        self.center = Point(5, 5)
        while self.game_map[self.center.x][self.center.y].ground == 'water':
            self.center.x += 1
            self.center.y += 1
        self.game_map[self.center.x][self.center.y].building = 'center'

    def __init__(self):
        self.drag = False
        self.popup_active = False
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
        self.monsters = [Monster(self.game_map)]
        self.game_map[0][0].unit = self.monsters[0]
        self.specialists = [Specialist(specialist.CHIEFTAIN)]
        self.last_time = time.time() * 1000
        self.accum = 0

    def send_expedition(self):
        self.uis.show_chose_specialists_dialog()

    def destroy_expedition(self, monster_tile):
        expedition = monster_tile.unit
        expedition.status = expedition.DEAD
        for spec in expedition.warriors + expedition.workers:
            self.specialists.remove(spec)


    def move_monsters(self):
        for monster in self.monsters:
            self.game_map[monster.x][monster.y].unit = None
            monster.move()

            monster_tile = self.game_map[monster.x][monster.y]
            if monster_tile.unit:
                self.destroy_expedition(monster_tile)
            monster_tile.unit = monster

    def move_expeditions(self):
        for expedition_item in self.expeditions:
            self.game_map[expedition_item.x][expedition_item.y].unit = None
            expedition_item.make_move()
            tile = self.game_map[expedition_item.x][expedition_item.y]
            if type(tile.unit) == Monster:
                expedition_item.status = expedition.DEAD
            elif expedition_item.status == expedition.FINISHED:
                self.village.change_resource_count(expedition_item.resource, 100)
            else:
                tile.unit = expedition_item
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

        for cond in bc.tile_params:
            if cond != self.game_map[x][y].resource:
                return

        if not self.check_nearby_tiles(x, y, bc.near):
            return

        for resource in bc.resources:
            self.village.change_resource_count(resource, -bc.resources[resource])

        for resource in bc.changes:
            self.village.change_resource_count(resource, bc.changes[resource])

        self.game_map[x][y].building = self.uis.building

    #Conditions for nearby tiles. Specially for port building
    def check_nearby_tiles(self, x, y, cond):
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

    def process(self):
        curr_time = time.time() * 1000
        delta = curr_time - self.last_time
        self.last_time = curr_time
        self.accum += delta

        if self.accum >= 100:
            self.accum -= 100
            self.dx += self.scroll_spd_x
            self.dy += self.scroll_spd_y
