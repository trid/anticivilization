__author__ = 'TriD'


class BuildConditions:
    def __init__(self, conditions={}, changes=()):
        self.resources = conditions.get('resources', [])
        self.tile_params = conditions.get('tile_params', [])
        self.near = conditions.get('near', [])
        self.changes = changes