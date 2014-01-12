from pygame.surface import Surface
from ui.clickable import Clickable

__author__ = 'TriD'


class Dialog(object):
    def __init__(self, x, y, w, h):
        self.items = []
        self.clickables = []
        self.surface = Surface((w, h))
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.enter_btn = None
        self.esc_btn = None

    def draw(self, screen):
        self.surface.fill(0xaaaaaa)
        for item in self.items:
            item.draw(self.surface)
        screen.blit(self.surface, (self.x, self.y))

    def add(self, item):
        self.items.append(item)
        if isinstance(item, Clickable):
            self.clickables.append(item)

    def click(self, wx, wy):
        x = wx - self.x
        y = wy - self.y
        if x < 0 or y < 0:
            return
        for item in self.clickables:
            item.is_pressed(x, y)

    def add_ok(self, button):
        self.enter_btn = button
        self.add(button)

    def add_cancel(self, button):
        self.esc_btn = button
        self.add(button)