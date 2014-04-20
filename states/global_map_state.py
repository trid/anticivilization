import pickle
from display import Display
from events import EventProcessor
from game_data import GameData
from ui_state import UIState

__author__ = 'TriD'


class GlobalMapState:
    def __init__(self):
        self.game_data = GameData()
        self.display = Display(self.game_data)
        self.uis = UIState(self.game_data)
        self.events = EventProcessor(self.game_data, self.uis, self.display)
        #Building buttons callbacks
        self.uis.button_homes.callback = self.generate_building_callback('houses')
        self.uis.button_fields.callback = self.generate_building_callback('field')
        self.uis.button_woodcutter.callback = self.generate_building_callback('woodcutter')
        self.uis.button_road.callback = self.generate_building_callback('road')
        self.uis.button_port.callback = self.generate_building_callback('port')
        self.uis.button_stockpile.callback = self.generate_building_callback('stockpile')
        self.uis.button_stone_carrier.callback = self.generate_building_callback('stone_carrier')
        self.uis.button_workshop.callback = self.generate_building_callback('workshop')
        self.uis.button_destruct.callback = self.generate_building_callback('destruct')
        self.display.uis = self.uis
        self.game_data.uis = self.uis
        self.uis.save_button.callback = self.save_game
        self.uis.load_button.callback = self.load_game


    def process(self):
        self.game_data.process()
        self.events.process_events()
        self.display.draw()

    def generate_building_callback(self, building):
        def callback():
            self.uis.building = building
        return callback

    def load_game(self):
        self.game_data.uis = None
        with open('../save', 'rb') as save_file:
            self.game_data = pickle.load(save_file)
        self.game_data.uis = self.uis
        self.display.reset_game_data(self.game_data)
        self.events.data = self.game_data

    def save_game(self):
        self.game_data.uis = None
        with open('../save', 'wb') as save_file:
            pickle.dump(self.game_data, save_file)
        self.game_data.uis = self.uis