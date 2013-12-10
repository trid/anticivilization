from GameData import GameData
from display import Display
from events import EventProcessor
__author__ = 'TriD'

import pygame
from ui_state import UIState

game_data = GameData()
uis = UIState(game_data)
game_data.uis = uis
display = Display(game_data, uis)
event_processor = EventProcessor(game_data, uis)


def build_houses():
    uis.building = 'houses'


def build_field():
    uis.building = 'field'


def build_woodcutter():
    uis.building = 'woodcutter'


def send_expedition_callback():
    game_data.send_expedition()

uis.button_homes.callback = build_houses
uis.button_fields.callback = build_field
uis.button_woodcutter.callback = build_woodcutter
uis.button_expedition.callback = send_expedition_callback


while not game_data.done:
    event_processor.process_events()
    display.draw()