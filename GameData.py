from expedition import Expedition
from game_map import GameMap
from monster import Monster
from village import Village

__author__ = 'TriD'


class GameData():
    def __init__(self):
        self.drag = False
        self.old_dx = 0
        self.old_dy = 0
        self.dx = 0
        self.dy = 0
        self.buttons_active = False
        self.done = False
        self.game_map = GameMap()
        self.exp_pos = None
        self.village = Village()
        self.expeditions = []
        self.turn = 0
        self.monster = Monster()

    def send_expedition(self):
        if self.village.food_stockpile >= 100:
            expedition = Expedition()
            expedition.find_path(5, 5, self.exp_pos[0], self.exp_pos[1], [])
            self.expeditions.append(expedition)
            self.village.food_stockpile -= 100
            
    def next_turn(self):
        self.turn += 1
        self.village.update()
        for expedition in self.expeditions:
            expedition.move()
            if expedition.returned:
                self.village.wood_stockpile += 100
        self.expeditions = filter(lambda x: not x.returned, self.expeditions)
        self.monster.random_move()

    def build(self, mouse_x, mouse_y):
        x = (mouse_x - self.dx - self.dx % 32) / 32
        y = (mouse_y - self.dy - self.dy % 32) / 32

        may_build = False
        if self.game_map[x][y].building:
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
        if self.uis.building == 'field':
            self.village.food_growth += 600
        elif self.uis.building == 'houses':
            self.village.max_population += 400
        elif self.uis.building == 'woodcutter':
            if self.game_map[x][y].resource != 'tree':
                return
            else:
                self.village.wood_increasing += 100
        self.game_map[x][y].building = self.uis.building
