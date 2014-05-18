from pygame.surface import Surface
from ui.clickable import Clickable

__author__ = 'TriD'


class Panel(Clickable):
    def __init__(self, x, y, w, h, color=0x000000):
        self.items = []
        self.clickables = []
        self.surface = Surface((w, h))
        self.visible = True
        self.x = x
        self.y = y
        self.color = color

    def draw(self, screen):
        if self.visible:
            self.surface.fill(self.color)
            for item in self.items:
                item.draw(self.surface)
            screen.blit(self.surface, (self.x, self.y))

    def add(self, item):
        self.items.append(item)
        if isinstance(item, Clickable):
            self.clickables.append(item)

    def is_pressed(self, wx, wy, button):
        if not self.visible:
            return False
        x = wx - self.x
        y = wy - self.y
        res = False
        for item in self.clickables:
            res = res or item.is_pressed(x, y, button)
        return res