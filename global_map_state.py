from display import Display
from events import EventProcessor
from game_data import GameData
from ui_state import UIState

__author__ = 'TriD'


class GlobalMapState:
    def __init__(self):
        self.game_data = GameData()
        self.display = Display()
        self.uis = UIState()
        self.events = EventProcessor(self.game_data, self.uis, self.display)

    def process(self):
        self.game_data.process()
        self.events.process_events()
        self.display.draw()