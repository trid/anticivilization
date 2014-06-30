import pickle
import pygame
from display import Display
import event_manager
from game_data import GameData
from ui_state import UIState

__author__ = 'TriD'


class GlobalMapState:
    def initialize_interface(self):
        self.display = Display(self.game_data)
        self.uis = UIState(self.game_data)
        #Building buttons callbacks
        self.uis.button_homes.callback = self.generate_building_callback('houses')
        self.uis.button_fields.callback = self.generate_building_callback('field')
        self.uis.button_woodcutter.callback = self.generate_building_callback('woodcutter')
        self.uis.button_road.callback = self.generate_building_callback('road')
        self.uis.button_port.callback = self.generate_building_callback('port')
        self.uis.button_stockpile.callback = self.generate_building_callback('stockpile')
        self.uis.button_stone_carrier.callback = self.generate_building_callback('stone_carrier')
        self.uis.button_workshop.callback = self.generate_building_callback('workshop')
        self.uis.button_iron_mine.callback = self.generate_building_callback('iron_mine')
        self.uis.button_destruct.callback = self.generate_building_callback('destruct')
        self.display.uis = self.uis
        self.game_data.uis = self.uis
        self.uis.display = self.display
        self.uis.save_button.callback = self.save_game
        self.uis.load_button.callback = self.load_game
        #Listeners
        event_manager.event_manager.add_listener(event_manager.MESSAGE_MOUSE_UP, self.uis.mouse_button_up_callback)
        event_manager.event_manager.add_listener(event_manager.MESSAGE_KEY_UP, self.keyup_callback)
        event_manager.event_manager.add_listener(event_manager.MESSAGE_KEY_DOWN, self.keydown_callback)
        event_manager.event_manager.add_listener(event_manager.MESSAGE_MOUSE_MOTION, self.mouse_move)
        event_manager.event_manager.add_listener(event_manager.MESSAGE_MOUSE_DOWN, self.mouse_key_down_callback)
        event_manager.event_manager.add_listener(event_manager.MESSAGE_KEY_UP, self.uis.check_button_up)

    def remove_listeners(self):
        event_manager.event_manager.remove_listener(event_manager.MESSAGE_MOUSE_UP, self.uis.mouse_button_up_callback)
        event_manager.event_manager.remove_listener(event_manager.MESSAGE_KEY_UP, self.keyup_callback)
        event_manager.event_manager.remove_listener(event_manager.MESSAGE_KEY_DOWN, self.keydown_callback)
        event_manager.event_manager.remove_listener(event_manager.MESSAGE_MOUSE_MOTION, self.mouse_move)
        event_manager.event_manager.remove_listener(event_manager.MESSAGE_MOUSE_DOWN, self.mouse_key_down_callback)
        event_manager.event_manager.remove_listener(event_manager.MESSAGE_KEY_UP, self.uis.check_button_up)

    def __init__(self):
        self.game_data = None

    def process(self):
        self.game_data.process()
        self.display.draw()

    def generate_building_callback(self, building):
        def callback():
            self.uis.building = building
        return callback

    def keyup_callback(self, key):
        if not self.uis.dialog:
            if key == pygame.K_RETURN:
                self.game_data.next_turn()
            if key == pygame.K_ESCAPE:
                self.uis.dialog = self.uis.main_menu
        else:
            if key == pygame.K_RETURN:
                if self.uis.dialog.enter_btn:
                    self.uis.dialog.enter_btn.run_callback()
            elif key == pygame.K_ESCAPE:
                if self.uis.dialog.esc_btn:
                    self.uis.dialog.esc_btn.run_callback()
        if key == pygame.K_UP or key == pygame.K_DOWN:
            self.game_data.scroll_spd_y = 0
        if key == pygame.K_LEFT or key == pygame.K_RIGHT:
            self.game_data.scroll_spd_x = 0

    def keydown_callback(self, key):
        if key == pygame.K_UP:
            self.game_data.scroll_spd_y = -5
        if key == pygame.K_LEFT:
            self.game_data.scroll_spd_x = -5
        if key == pygame.K_DOWN:
            self.game_data.scroll_spd_y = 5
        if key == pygame.K_RIGHT:
            self.game_data.scroll_spd_x = 5

    def mouse_move(self, pos_x, pos_y):
        self.display.mouse_x, self.display.mouse_y = pos_x, pos_y
        if self.game_data.drag:
            #And here we move the map on the screen
            mouse_pos_x, mouse_pos_y = pos_x, pos_y
            self.game_data.dx = self.game_data.old_dx + (mouse_pos_x - self.game_data.mouse_drag_x)
            self.game_data.dy = self.game_data.old_dy + (mouse_pos_y - self.game_data.mouse_drag_y)
        else:
            if pos_x < 10:
                self.game_data.scroll_spd_x = -5
            elif 590 < pos_x < 600:
                self.game_data.scroll_spd_x = 5
            else:
                self.game_data.scroll_spd_x = 0
            if pos_y < 10:
                self.game_data.scroll_spd_y = -5
            elif pos_y > 590:
                self.game_data.scroll_spd_y = 5
            else:
                self.game_data.scroll_spd_y = 0

    def mouse_key_down_callback(self, pos_x, pos_y, button):
        if button == 1 and pos_x < 600 and not self.uis.dialog:
            #Here we start drag the map
            self.game_data.drag = True
            self.game_data.mouse_drag_x, self.game_data.mouse_drag_y = pos_x, pos_y
            self.game_data.old_dx = self.game_data.dx
            self.game_data.old_dy = self.game_data.dy

    def load_game(self, from_start_menu=False):
        if not from_start_menu:
            self.remove_listeners()
        with open('../save', 'rb') as save_file:
            self.game_data = pickle.load(save_file)
        self.initialize_interface()


    def save_game(self):
        self.game_data.uis = None
        with open('../save', 'wb') as save_file:
            pickle.dump(self.game_data, save_file)
        self.game_data.uis = self.uis

    def new_game(self):
        self.game_data = GameData()
        self.display = Display(self.game_data)
        self.uis = UIState(self.game_data)
        self.initialize_interface()
