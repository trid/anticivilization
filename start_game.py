__author__ = 'TriD'

from game_data import GameData
from display import Display
from events import EventProcessor
from ui_state import UIState

game_data = GameData()
display = Display(game_data)
uis = UIState(game_data)
display.uis = uis
game_data.uis = uis
event_processor = EventProcessor(game_data, uis, display)


def build_houses():
    uis.building = 'houses'


def build_field():
    uis.building = 'field'


def build_woodcutter():
    uis.building = 'woodcutter'


def build_road():
    uis.building = 'road'


def build_port():
    uis.building = 'port'


def build_stockpile():
    uis.building = 'stockpile'


def build_stone_carrier():
    uis.building = 'stone_carrier'


def build_workshop():
    uis.building = 'workshop'


def destruct_building():
    uis.building = 'destruct'


uis.button_homes.callback = build_houses
uis.button_fields.callback = build_field
uis.button_woodcutter.callback = build_woodcutter
uis.button_road.callback = build_road
uis.button_port.callback = build_port
uis.button_stockpile.callback = build_stockpile
uis.button_stone_carrier.callback = build_stone_carrier
uis.button_workshop.callback = build_workshop
uis.button_destruct.callback = destruct_building

while not game_data.done:
    game_data.process()
    event_processor.process_events()
    display.draw()