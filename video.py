import pygame

__author__ = 'TriD'


class Video:
    def __init__(self):
        pygame.init()
        screen_size = (800, 600)
        self.screen = pygame.display.set_mode(screen_size)

    def draw(self, sprite, position):
        pass

    def flip(self):
        pygame.display.flip()

    def clean(self):
        self.screen.fill((0, 0, 0))

video = Video()