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
           'houses': pygame.image.load('res/images/houses.png'),
           'field': pygame.image.load('res/images/field.png'),
           'human': pygame.image.load('res/images/human.png'),
           'tree': pygame.image.load('res/images/tree.png')}
        self.button_homes = Button(0, 0, 115, 23)
        self.button_fields = Button(0, 0, 93, 23)