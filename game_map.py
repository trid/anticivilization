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
        start_map = []

        for i in range(0, 10):
            start_map.append([Tile() for k in range(0, 10)])

        start_map[5][5].building = 'center'
        start_map[9][9].resource = 'tree'

        self.data = {(0, 0): start_map}

    def __getitem__(self, row):
        return Column(self, row)

    def get_tile(self, x, y):
        return self.data[(0, 0)][x][y]

    def set_tile(self, x, y, tile):
        self.data[(0, 0)][x][y] = tile