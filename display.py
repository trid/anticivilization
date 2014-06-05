import pygame
from field_view import FieldView
from sprite_manager import SpriteManager
from video import video

__author__ = 'TriD'


class Display():
    def __init__(self, game_data, uis=None):
        self.screen = video.screen
        self.game_data = game_data
        self.uis = uis
        self.mouse_x, self.mouse_y = 0, 0
        self.sm = SpriteManager()
        self.field_view = FieldView(self.game_data)

    def draw(self):
        self.screen.fill((0, 0, 0))

        self.field_view.mouse_x, self.field_view.mouse_y = self.mouse_x, self.mouse_y
        self.field_view.draw_field(self.screen)

        self.uis.update_labels()
        self.uis.draw(self.screen)

        pygame.display.flip()

    def reset_game_data(self, game_data):
        self.game_data = game_data
        self.field_view.game_data = game_data