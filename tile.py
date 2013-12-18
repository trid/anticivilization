__author__ = 'TriD'


class Tile:
    def __init__(self):
        self.building = None
        #Ground can be 'grass' or 'water'
        self.ground = 'grass'
        self.resource = None
        self.unit = None