import pygame

__author__ = 'TriD'


class Video:
    def __init__(self):
        screen_size = (800, 600)
        self.screen = pygame.display.set_mode(screen_size)

    def draw(self, sprite, position):
        pass

video = Video()