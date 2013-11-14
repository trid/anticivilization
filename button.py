__author__ = 'TriD'


class Button:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.callback = None
        self.active = True

    def is_pressed(self, x, y):
        if not self.active:
            return False
        if x < self.x:
            return False
        elif x > self.x + self.w:
            return False
        elif y < self.y:
            return False
        elif y > self.y + self.h:
            return False

        if self.callback:
            self.callback()

        return True