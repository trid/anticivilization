from pygame.surface import Surface

__author__ = 'TriD'


class Dialog(object):
    def __init__(self, x, y, w, h):
        self.items = []
        self.surface = Surface((w, h))
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def draw(self, screen):
        for item in self.items:
            item.draw(self.surface)
        screen.blit(self.surface, (self.x, self.y))