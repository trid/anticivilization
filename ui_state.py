__author__ = 'trid'

import pygame
from button import Button


class UIState:
    def __init__(self):
        self.building = None
        self.sprites = {'center': pygame.image.load('res/images/center.png'),
                        'grass': pygame.image.load('res/images/grass.png'),
                        'build_homes': pygame.image.load('res/images/build_homes.png'),
                        'build_field': pygame.image.load('res/images/build_field.png'),
                        'build_woodcutter': pygame.image.load('res/images/build_woodcutter.png'),
                        'send_expedition': pygame.image.load('res/images/send_expedition.png'),
                        'houses': pygame.image.load('res/images/houses.png'),
                        'field': pygame.image.load('res/images/field.png'),
                        'human': pygame.image.load('res/images/human.png'),
                        'tree': pygame.image.load('res/images/tree.png'),
                        'woodcutter': pygame.image.load('res/images/woodcutter.png')}
        self.button_homes = Button(0, 0, 115, 23, 'build_homes')
        self.button_fields = Button(0, 0, 93, 23, 'build_field')
        self.button_woodcutter = Button(0, 0, 140, 21, 'build_woodcutter')
        self.button_expedition = Button(0, 0, 132, 21, 'send_expedition')

        self.grass_click_buttons = [self.button_homes, self.button_fields, self.button_woodcutter]
        self.resource_click_buttons = self.grass_click_buttons + [self.button_expedition]
        self.button_set = None

    def setup_buttons(self, x, y):
        self.button_homes.x = x
        self.button_homes.y = y
        self.button_fields.x = x
        self.button_fields.y = y + 23
        self.button_woodcutter.x = x
        self.button_woodcutter.y = y + 46
        self.button_expedition.x = x
        self.button_expedition.y = y + 67

    def set_grass_click(self):
        self.button_set = self.grass_click_buttons

    def set_resource_click_buttons(self):
        self.button_set = self.resource_click_buttons

    def draw_buttons(self, screen):
        y = self.button_homes.y

        for button in self.button_set:
            screen.blit(self.sprites[button.name], (button.x, button.y))