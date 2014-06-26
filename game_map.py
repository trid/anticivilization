import random
from map_gen.river import River
from map_gen.simplexnoise import raw_noise_2d, octave_noise_2d
from tile import Tile

SQUARE_HEIGHT = 10

SQUARE_WIDTH = 10

MAP_HEIGHT = 20

MAP_WIDTH = 20

__author__ = 'TriD'


class Column:
    def __init__(self, game_map, row):
        self.game_map = game_map
        self.row = row

    def __getitem__(self, item):
        return self.game_map.get_tile(self.row, item)

    def __setitem__(self, key, value):
        self.game_map.set_tile(self.row, key, value)


class GameMap:
    def __init__(self):
        self.data = {}

    def __getitem__(self, row):
        return Column(self, row)

    def get_tile(self, x, y):
        sx = (x / SQUARE_WIDTH) % MAP_WIDTH
        sy = (y / SQUARE_HEIGHT) % MAP_HEIGHT
        self.touch_square(sx, sy)
        return self.data[(sx, sy)][x % SQUARE_WIDTH][y % SQUARE_WIDTH]

    def set_tile(self, x, y, tile):
        sx = (x / SQUARE_WIDTH) % MAP_WIDTH
        sy = (y / SQUARE_HEIGHT) % MAP_HEIGHT
        self.touch_square(sx, sy)
        self.data[(sx, sy)][x % SQUARE_WIDTH][y % SQUARE_HEIGHT] = tile

    def touch_square(self, x, y):
        if not (x, y) in self.data:
            data = []
            for i in range(0, SQUARE_WIDTH):
                row = []
                for k in range(0, SQUARE_HEIGHT):
                    tile = Tile()
                    row.append(tile)
                data.append(row)
            self.data[(x, y)] = data

    def generate_rivers(self, x, y):
        pass