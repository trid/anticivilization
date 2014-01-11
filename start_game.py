from map_gen.river_gen import generate_rivers

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
generate_rivers(game_data.game_map)


def build_houses():
    uis.building = 'houses'


def build_field():
    uis.building = 'field'


def build_woodcutter():
    uis.building = 'woodcutter'


def build_road():
    uis.building = 'road'


def send_expedition_callback():
    game_data.send_expedition()

uis.button_homes.callback = build_houses
uis.button_fields.callback = build_field
uis.button_woodcutter.callback = build_woodcutter
uis.button_expedition.callback = send_expedition_callback
uis.button_road.callback = build_road()

while not game_data.done:
    event_processor.process_events()
    display.draw()