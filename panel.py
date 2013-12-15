from ui.clickable import Clickable

__author__ = 'TriD'


class Panel:
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

    def click(self, x, y):
        res = False
        for item in self.items:
            res = res or item.is_pressed(x, y)