import json
import os
from build_conditions import BuildConditions

RES_BUILDINGS = 'res/buildings'

__author__ = 'TriD'


class BuildingManager(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(BuildingManager, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.conds = {}
        for item in os.listdir(RES_BUILDINGS):
            name = os.path.splitext(item)
            datafile = open("%s/%s" % (RES_BUILDINGS, item))
            data = json.load(datafile)
            bc = BuildConditions(data['resources'], data.get('tile_params', []), data['growth'])
            self.conds[name[0]] = bc
