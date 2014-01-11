from building_manager import BuildingManager
import expedition
from game_map import GameMap
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
        self.game_map[5][5].building = 'center'
        self.center = Point(5, 5)

    def __init__(self):
        self.drag = False
        self.popup_active = False
        self.done = False
        self.game_map = GameMap()
        self.place_center()
        self.place_resources()
        self.old_dx = 0
        self.old_dy = 0
        self.dx = -(300 - 32 * self.center.x)
        self.dy = -(300 - 32 * self.center.y)
        self.exp_pos = None
        self.village = Village()
        self.expeditions = []
        self.turn = 0
        self.monsters = [Monster()]
        self.game_map[0][0].unit = self.monsters[0]
        self.specialists = [Specialist(specialist.CHIEFTAIN)]

    def send_expedition(self):
        self.uis.show_chose_specialists_dialog()

    def move_monsters(self):
        for monster in self.monsters:
            self.game_map[monster.x][monster.y].unit = None
            monster.random_move()

            monster_tile = self.game_map[monster.x][monster.y]
            if monster_tile.unit:
                monster_tile.unit.status = expedition.DEAD
            monster_tile.unit = monster

    def next_turn(self):
        self.turn += 1
        self.village.update()
        for expedition_item in self.expeditions:
            self.game_map[expedition_item.x][expedition_item.y].unit = None
            expedition_item.move()
            tile = self.game_map[expedition_item.x][expedition_item.y]
            if type(tile.unit) == Monster:
                expedition_item.status = expedition.DEAD
            elif expedition_item.status == expedition.FINISHED:
                self.village.wood_stockpile += 100
            else:
                tile.unit = expedition_item
        self.expeditions = filter(lambda x: x.status != expedition.FINISHED and x.status != expedition.DEAD, self.expeditions)
        self.move_monsters()

    def build(self, mouse_x, mouse_y):
        x = (self.dx + mouse_x) / 32
        y = (self.dy + mouse_y) / 32

        may_build = False
        if self.game_map[x][y].building:
            return
        if self.game_map[x][y].ground == 'water':
            return
        if x > 0:
            if self.game_map[x - 1][y].building:
                may_build = True
            if y > 0 and self.game_map[x - 1][y - 1].building:
                may_build = True
            if y < 9 and self.game_map[x - 1][y - 1].building:
                may_build = True
        if x < 9:
            if self.game_map[x + 1][y].building:
                may_build = True
            if y > 0 and self.game_map[x + 1][y - 1].building:
                may_build = True
            if y < 9 and self.game_map[x + 1][y + 1].building:
                may_build = True
        if y > 0 and self.game_map[x][y - 1].building:
            may_build = True
        if y < 9 and self.game_map[x][y + 1].building:
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

        for cond in bc.near:
            self.check_nearby_tiles(x, y, cond)

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
                result = getattr(point) == cond[param] or result
            if not result:
                return False
        return True