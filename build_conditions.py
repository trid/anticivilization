__author__ = 'TriD'


class BuildConditions:
    def __init__(self, resources={}, tile_params=[], changes=[]):
        self.resources = resources
        self.tile_params = tile_params
        self.changes = changes