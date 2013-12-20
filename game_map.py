import random
from map_gen.river import River
from map_gen.simplexnoise import raw_noise_2d, octave_noise_2d
from tile import Tile

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
        self.touch_square(0, 0)
        start_map = self.data[(0, 0)]

        start_map[5][5].building = 'center'
        start_map[9][9].resource = 'tree'

        self.river = River(random.randint(0, 500), random.randint(0, 500))

    def __getitem__(self, row):
        return Column(self, row)

    def get_tile(self, x, y):
        self.touch_square(x / 10, y / 10)
        return self.data[(x / 10, y / 10)][x % 10][y % 10]

    def set_tile(self, x, y, tile):
        self.touch_square(x / 10, y / 10)
        self.data[(x / 10, y / 10)][x % 10][y % 10] = tile

    def touch_square(self, x, y):
        if not (x, y) in self.data:
            self.generate_rivers(x, y)
            data = []
            for i in range(0, 10):
                row = []
                for k in range(0, 10):
                    tile = Tile()
                    tile.ground = 'grass' if octave_noise_2d(5, 1, 1, i * 10 + x, k * 10 + y) >= -0.1 else 'water'
                    row.append(tile)
                data.append(row)
            self.data[(x, y)] = data

    def generate_rivers(self, x, y):
        pass