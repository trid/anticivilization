__author__ = 'TriD'


class Panel:
    def __init__(self):
        self.items = []
        self.visible = True

    def draw(self, screen):
        if self.visible:
            for item in self.items:
                item.draw(screen)

    def add(self, item):
        self.items.append(item)