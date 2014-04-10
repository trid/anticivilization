import pickle
from global_map_state import GlobalMapState

__author__ = 'TriD'


state = GlobalMapState()

while not state.game_data.done:
    state.process()