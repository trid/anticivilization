from application import application
import event_manager
from sprite_manager import SpriteManager
from states.global_map_state import GlobalMapState
from ui.button import Button
from video import video


__author__ = 'TriD'


class StartMenuState:
    def __init__(self):
        self.sm = SpriteManager()
        self.button_new_game = Button(352, 0, 96, 23, sprite=self.sm.sprites['new_game_button'], callback=self.start_new_game)
        self.button_load_game = Button(378, 23, 44, 23, sprite=self.sm.sprites['load_button'], callback=self.load_game)
        self.button_exit = Button(378, 46, 41, 23, sprite=self.sm.sprites['exit_button'], callback=self.exit_game)
        event_manager.event_manager.add_listener(event_manager.MESSAGE_MOUSE_UP, self)

    def process(self):
        self.button_new_game.draw(video.screen)
        self.button_load_game.draw(video.screen)
        self.button_exit.draw(video.screen)
        video.flip()

    def process_message(self, pos_x, pos_y, button):
        self.button_new_game.is_pressed(pos_x, pos_y, button)
        self.button_load_game.is_pressed(pos_x, pos_y, button)
        self.button_exit.is_pressed(pos_x, pos_y, button)

    def start_new_game(self):
        event_manager.event_manager.purge()
        state = GlobalMapState()
        state.new_game()
        application.push_state(state)

    def load_game(self):
        event_manager.event_manager.purge()
        state = GlobalMapState()
        state.load_game(from_start_menu=True)
        application.push_state(state)

    def exit_game(self):
        application.running = False