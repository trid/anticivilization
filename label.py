import pygame

__author__ = 'TriD'


class Label:
    def __init__(self, x, y, text, h = 18):
        self.x = x
        self.y = y
        self.dirty = True
        self.text = text
        self.h = h
        self.surface = None
        self.font = pygame.font.SysFont('monospace', h)

    def draw(self, screen):
        if self.dirty:
            self.surface = self.font.render(self.text, 1, (255, 255, 255))
            self.dirty = False
        screen.blit(self.surface, (self.x, self.y))

    def set_text(self, text):
        self.text = text
        self.dirty = True