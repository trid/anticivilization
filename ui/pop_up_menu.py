from pygame.surface import Surface
from ui.clickable import Clickable

__author__ = 'TriD'


class PopUpMenu(Clickable):
    def __init__(self):
        self.visible = False
        self.items = []
        self.x, self.y, self.w, self.h = (0, 0, 0, 0)
        self.surface = False
        self.dirty = True

    def is_pressed(self, x, y):
        if not self.visible:
            return False
        if x < self.x:
            return False
        elif x > self.x + self.w:
            return False
        elif y < self.y:
            return False
        elif y > self.y + self.h:
            return False

        res = False
        for item in self.items:
            res = res or item.is_pressed(x, y)
        return res

    def show(self, x, y):
        self.x = x
        self.y = y
        self.visible = True

    def hide(self):
        self.visible = False

    def add_item(self, item):
        self.items.append(item)
        item.x = 0
        item.y = self.h
        self.h += item.h
        if self.w < item.w:
            self.w = item.w
        self.dirty = True

    def draw(self, screen):
        if not self.visible:
            return
        if self.dirty:
            self.surface = Surface((self.w, self.h))
            for item in self.items:
                item.draw(self.surface)
            self.dirty = False
        screen.blit(self.surface, (self.x, self.y))
