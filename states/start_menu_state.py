from sprite_manager import SpriteManager
from ui.button import Button
from video import video


__author__ = 'TriD'


class StartMenuState:
    def __init__(self):
        self.sm = SpriteManager()
        self.button_new_game = Button(352, 0, 96, 23, sprite=self.sm.sprites['new_game_button'])
        self.button_load_game = Button(378, 23, 44, 23, sprite=self.sm.sprites['load_button'])
        self.button_exit = Button(378, 46, 41, 23, sprite=self.sm.sprites['exit_button'])

    def process(self):
        self.button_new_game.draw(video.screen)
        self.button_load_game.draw(video.screen)
        self.button_exit.draw(video.screen)
        video.flip()