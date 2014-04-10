import pickle
from global_map_state import GlobalMapState

__author__ = 'TriD'


state = GlobalMapState()

state.display.uis = state.uis
state.game_data.uis = state.uis


def load_game():
    state.game_data.uis = None
    with open('save', 'rb') as save_file:
        state.game_data = pickle.load(save_file)
    state.game_data.uis = state.uis
    state.display.reset_game_data(state.game_data)
    state.event_processor.data = state.game_data


def save_game():
    state.game_data.uis = None
    with open('save', 'wb') as save_file:
        pickle.dump(state.game_data, save_file)
    state.game_data.uis = state.uis


state.uis.save_button.callback = save_game
state.uis.load_button.callback = load_game

while not state.game_data.done:
    state.process()