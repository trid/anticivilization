__author__ = 'TriD'


class Tile:
    def __init__(self):
        self.building = None
        self.building_finished = False
        #Ground can be 'grass' or 'water' or 'swamp' or 'shit' or...
        self.ground = 'grass'
        self.resource = None
        self.units = []