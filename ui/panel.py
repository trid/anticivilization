from ui.clickable import Clickable

__author__ = 'TriD'


class Panel(Clickable):
    def __init__(self):
        self.items = []
        self.clickables = []
        self.visible = True

    def draw(self, screen):
        if self.visible:
            for item in self.items:
                item.draw(screen)

    def add(self, item):
        self.items.append(item)
        if isinstance(item, Clickable):
            self.clickables.append(item)

    def is_pressed(self, x, y):
        if not self.visible:
            return False
        res = False
        for item in self.clickables:
            res = res or item.is_pressed(x, y)
        return res